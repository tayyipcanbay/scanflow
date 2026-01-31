"""
Mesh upload API routes.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

from app.database.connection import get_db
from app.models.mesh import MeshUpload
from app.models.user import User
from app.utils.file_handler import FileHandler
from app.services.mesh_processor import MeshProcessor
from app.middleware.firebase_auth import get_current_user, get_optional_user
from app.services.firebase_integration import firebase_integration

router = APIRouter()
file_handler = FileHandler()
mesh_processor = MeshProcessor()


class MeshUploadResponse(BaseModel):
    """Response model for mesh upload."""
    id: int
    user_id: int
    file_path: str
    version: int
    is_baseline: bool
    upload_date: str


@router.post("/", response_model=MeshUploadResponse)
async def upload_mesh(
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None),  # Optional for backward compatibility
    firebase_uid: Optional[str] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Upload a 3D mesh file.
    
    Args:
        file: Mesh file (GLB/OBJ/FBX)
        user_id: User ID (optional, for backward compatibility)
        firebase_uid: Firebase user UID from authentication
        db: Database session
        
    Returns:
        Upload response with mesh metadata
    """
    # Validate file
    if not file_handler.validate_mesh_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid mesh file. Supported formats: GLB, OBJ, FBX. Max size: 100MB"
        )
    
    # Use Firebase UID if available, otherwise fall back to user_id
    # For now, map Firebase UID to a numeric user_id (in production, use a proper mapping)
    if firebase_uid:
        # Get or create user mapping
        # In production, you'd have a User table that maps firebase_uid to user_id
        user = db.query(User).filter(User.email == f"{firebase_uid}@firebase").first()
        if not user:
            # Create user with Firebase UID
            user = User(
                email=f"{firebase_uid}@firebase",
                username=firebase_uid[:20],  # Use first 20 chars of UID
                hashed_password="firebase_auth"  # Not used with Firebase Auth
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        user_id = user.id
    elif user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide Firebase token or user_id."
        )
    
    # Check if user exists (for backward compatibility)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Create default user for testing
        user = User(
            id=user_id,
            email=f"user{user_id}@example.com",
            username=f"user{user_id}",
            hashed_password="dummy"
        )
        db.add(user)
        db.commit()
    
    # Check if this is the first upload (baseline)
    existing_uploads = db.query(MeshUpload).filter(
        MeshUpload.user_id == user_id
    ).all()
    
    is_baseline = len(existing_uploads) == 0
    version = len(existing_uploads) + 1
    
    # Save file
    file_path = await file_handler.save_mesh_file(file, user_id, version)
    
    # Validate mesh structure
    try:
        mesh_data = mesh_processor.process_mesh_file(file_path)
    except Exception as e:
        # Delete file if invalid
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid mesh structure: {str(e)}"
        )
    
    # If this is baseline, mark previous baselines as non-baseline
    if is_baseline:
        db.query(MeshUpload).filter(
            MeshUpload.user_id == user_id,
            MeshUpload.is_baseline == True
        ).update({"is_baseline": False})
    
    # Create database record
    mesh_upload = MeshUpload(
        user_id=user_id,
        file_path=str(file_path),
        version=version,
        is_baseline=is_baseline
    )
    
    db.add(mesh_upload)
    db.commit()
    db.refresh(mesh_upload)
    
    # Sync to Firebase Digital Twin if Firebase UID available
    if firebase_uid:
        try:
            # Extract basic metrics from mesh (simplified - in production, use actual analysis)
            mesh_metrics = {
                "file_path": str(file_path),
                "weight": 75.0,  # TODO: Extract from mesh or user input
                "body_fat": 18.5,
                "muscle_mass": 42.1,
                "bmi": 23.4,
                "bmr": 1800,
            }
            
            # Sync to Firebase
            firebase_integration.sync_mesh_to_digital_twin(
                user_id=firebase_uid,
                mesh_data=mesh_metrics
            )
        except Exception as e:
            # Log but don't fail the upload
            import logging
            logging.error(f"Failed to sync to Firebase: {e}")
    
    return MeshUploadResponse(
        id=mesh_upload.id,
        user_id=mesh_upload.user_id,
        file_path=mesh_upload.file_path,
        version=mesh_upload.version,
        is_baseline=mesh_upload.is_baseline,
        upload_date=mesh_upload.upload_date.isoformat() if mesh_upload.upload_date else ""
    )


@router.get("/user/{user_id}")
async def list_user_meshes(
    user_id: int,
    db: Session = Depends(get_db)
):
    """List all mesh uploads for a user."""
    meshes = db.query(MeshUpload).filter(
        MeshUpload.user_id == user_id
    ).order_by(MeshUpload.version).all()
    
    return [
        {
            "id": m.id,
            "version": m.version,
            "is_baseline": m.is_baseline,
            "upload_date": m.upload_date.isoformat() if m.upload_date else ""
        }
        for m in meshes
    ]

