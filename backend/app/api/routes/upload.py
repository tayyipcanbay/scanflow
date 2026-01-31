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
    user_id: int = Form(1),  # TODO: Get from authentication
    db: Session = Depends(get_db)
):
    """
    Upload a 3D mesh file.
    
    Args:
        file: Mesh file (GLB/OBJ/FBX)
        user_id: User ID (temporary, should come from auth)
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
    
    # Check if user exists (for now, create if not exists)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Create default user for testing
        user = User(
            id=user_id,
            email=f"user{user_id}@example.com",
            username=f"user{user_id}",
            hashed_password="dummy"  # TODO: Proper authentication
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

