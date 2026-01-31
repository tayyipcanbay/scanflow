"""
Mesh comparison API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import json

from app.database.connection import get_db
from app.models.mesh import MeshUpload
from app.models.comparison import MeshComparison
from app.models.user import User
from app.services.mesh_comparator import MeshComparator
from app.services.region_detector import RegionDetector
from app.services.color_mapper import ColorMapper
from app.middleware.firebase_auth import get_optional_user
from app.services.firebase_integration import firebase_integration

router = APIRouter()
mesh_comparator = MeshComparator()
region_detector = RegionDetector()
color_mapper = ColorMapper()


class ComparisonResponse(BaseModel):
    """Response model for comparison."""
    id: int
    baseline_id: int
    comparison_id: int
    statistics: Dict[str, float]
    region_statistics: Dict[str, Dict[str, float]]
    color_data: Dict[str, Any]
    created_at: str


@router.get("/{baseline_id}/{comparison_id}", response_model=ComparisonResponse)
async def get_comparison(
    baseline_id: int,
    comparison_id: int,
    db: Session = Depends(get_db)
):
    """
    Get or create comparison between two meshes.
    
    Args:
        baseline_id: ID of baseline mesh
        comparison_id: ID of comparison mesh
        db: Database session
        
    Returns:
        Comparison result with statistics and color data
    """
    # Get mesh uploads
    baseline = db.query(MeshUpload).filter(MeshUpload.id == baseline_id).first()
    comparison_mesh = db.query(MeshUpload).filter(MeshUpload.id == comparison_id).first()
    
    if not baseline or not comparison_mesh:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both meshes not found"
        )
    
    if baseline.user_id != comparison_mesh.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Meshes must belong to the same user"
        )
    
    # Check if comparison already exists
    existing = db.query(MeshComparison).filter(
        MeshComparison.baseline_id == baseline_id,
        MeshComparison.comparison_id == comparison_id
    ).first()
    
    if existing:
        # Return existing comparison
        return ComparisonResponse(
            id=existing.id,
            baseline_id=existing.baseline_id,
            comparison_id=existing.comparison_id,
            statistics={
                "avg_magnitude": existing.avg_magnitude or 0.0,
                "max_magnitude": existing.max_magnitude or 0.0,
                "increase_percentage": existing.increase_percentage or 0.0,
                "decrease_percentage": existing.decrease_percentage or 0.0,
            },
            region_statistics=existing.displacement_data.get("region_statistics", {}),
            color_data=existing.displacement_data.get("color_data", {}),
            created_at=existing.created_at.isoformat() if existing.created_at else ""
        )
    
    # Perform comparison
    try:
        comparison_result = mesh_comparator.compare_mesh_files(
            baseline.file_path,
            comparison_mesh.file_path
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison failed: {str(e)}"
        )
    
    # Get statistics
    stats = mesh_comparator.get_displacement_statistics(comparison_result)
    
    # Detect regions and aggregate statistics
    region_stats = region_detector.aggregate_region_statistics(
        comparison_result["baseline_vertices"],
        comparison_result["displacements"],
        comparison_result["magnitudes"],
        comparison_result["projections"]
    )
    
    # Generate colors
    colors, color_metadata = color_mapper.map_displacement_to_colors_normalized(
        comparison_result["projections"],
        comparison_result["magnitudes"]
    )
    
    # Export color data
    color_data = color_mapper.export_color_data(
        colors,
        comparison_result["comparison_vertices"]
    )
    color_data.update(color_metadata)
    
    # Store comparison in database
    displacement_data = {
        "displacements": comparison_result["displacements"].tolist(),
        "magnitudes": comparison_result["magnitudes"].tolist(),
        "projections": comparison_result["projections"].tolist(),
        "directions": comparison_result["directions"].tolist(),
        "region_statistics": region_stats,
        "color_data": color_data
    }
    
    mesh_comparison = MeshComparison(
        baseline_id=baseline_id,
        comparison_id=comparison_id,
        displacement_data=displacement_data,
        avg_magnitude=stats["avg_magnitude"],
        max_magnitude=stats["max_magnitude"],
        increase_percentage=stats["increase_percentage"],
        decrease_percentage=stats["decrease_percentage"]
    )
    
    db.add(mesh_comparison)
    db.commit()
    db.refresh(mesh_comparison)
    
    # Sync comparison data to Firebase Digital Twin
    try:
        # Get Firebase UID from user (if available)
        # In production, you'd have a proper mapping table
        user = db.query(MeshUpload).filter(MeshUpload.id == baseline_id).first()
        if user:
            # Try to get Firebase UID from user email pattern
            user_obj = db.query(User).filter(User.id == user.user_id).first()
            if user_obj and "@firebase" in user_obj.email:
                firebase_uid = user_obj.email.replace("@firebase", "")
                
                # Sync comparison data
                comparison_payload = {
                    "statistics": {
                        "avg_magnitude": stats["avg_magnitude"],
                        "max_magnitude": stats["max_magnitude"],
                        "increase_percentage": stats["increase_percentage"],
                        "decrease_percentage": stats["decrease_percentage"],
                    },
                    "region_statistics": region_stats
                }
                
                firebase_integration.sync_mesh_to_digital_twin(
                    user_id=firebase_uid,
                    mesh_data={"file_path": comparison_mesh.file_path},
                    comparison_data=comparison_payload
                )
                
                # Trigger AI plan regeneration
                firebase_integration.trigger_ai_plan_regeneration(firebase_uid)
    except Exception as e:
        # Log but don't fail the comparison
        import logging
        logging.error(f"Failed to sync comparison to Firebase: {e}")
    
    return ComparisonResponse(
        id=mesh_comparison.id,
        baseline_id=mesh_comparison.baseline_id,
        comparison_id=mesh_comparison.comparison_id,
        statistics={
            "avg_magnitude": stats["avg_magnitude"],
            "max_magnitude": stats["max_magnitude"],
            "increase_percentage": stats["increase_percentage"],
            "decrease_percentage": stats["decrease_percentage"],
        },
        region_statistics=region_stats,
        color_data=color_data,
        created_at=mesh_comparison.created_at.isoformat() if mesh_comparison.created_at else ""
    )


@router.get("/user/{user_id}/latest")
async def get_latest_comparison(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get latest comparison for a user."""
    # Get baseline
    baseline = db.query(MeshUpload).filter(
        MeshUpload.user_id == user_id,
        MeshUpload.is_baseline == True
    ).first()
    
    if not baseline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No baseline mesh found"
        )
    
    # Get latest mesh
    latest_mesh = db.query(MeshUpload).filter(
        MeshUpload.user_id == user_id
    ).order_by(MeshUpload.version.desc()).first()
    
    if not latest_mesh or latest_mesh.id == baseline.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No comparison mesh found"
        )
    
    # Get comparison
    return await get_comparison(baseline.id, latest_mesh.id, db)

