"""
Insights API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.database.connection import get_db
from app.models.comparison import MeshComparison, BIAData
from app.models.insights import Insight
from app.services.insights_engine import InsightsEngine

router = APIRouter()
insights_engine = InsightsEngine(use_llm=False)  # Set to True and provide API key for LLM


class InsightResponse(BaseModel):
    """Response model for insights."""
    id: int
    comparison_id: int
    text: str
    confidence: float
    created_at: str


@router.get("/{comparison_id}", response_model=InsightResponse)
async def get_insights(
    comparison_id: int,
    db: Session = Depends(get_db)
):
    """
    Get or generate insights for a comparison.
    
    Args:
        comparison_id: Comparison ID
        db: Database session
        
    Returns:
        Generated insights
    """
    # Get comparison
    comparison = db.query(MeshComparison).filter(
        MeshComparison.id == comparison_id
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )
    
    # Check if insights already exist
    existing = db.query(Insight).filter(
        Insight.comparison_id == comparison_id
    ).first()
    
    if existing:
        return InsightResponse(
            id=existing.id,
            comparison_id=existing.comparison_id,
            text=existing.text,
            confidence=existing.confidence or 1.0,
            created_at=existing.created_at.isoformat() if existing.created_at else ""
        )
    
    # Get BIA data if available
    bia_data = None
    bia_record = db.query(BIAData).filter(
        BIAData.mesh_upload_id == comparison.comparison_id
    ).first()
    
    if bia_record:
        bia_data = {
            "weight": bia_record.weight,
            "bmi": bia_record.bmi,
            "fat_percentage": bia_record.fat_percentage,
            "muscle_percentage": bia_record.muscle_percentage,
            "water_percentage": bia_record.water_percentage,
        }
    
    # Generate insights
    displacement_data = comparison.displacement_data
    comparison_stats = {
        "avg_magnitude": comparison.avg_magnitude or 0.0,
        "max_magnitude": comparison.max_magnitude or 0.0,
        "increase_percentage": comparison.increase_percentage or 0.0,
        "decrease_percentage": comparison.decrease_percentage or 0.0,
    }
    region_stats = displacement_data.get("region_statistics", {})
    
    insights_result = insights_engine.generate_insights(
        comparison_stats,
        region_stats,
        bia_data
    )
    
    # Store insights
    insight = Insight(
        comparison_id=comparison_id,
        text=insights_result["text"],
        confidence=insights_result["confidence"]
    )
    
    db.add(insight)
    db.commit()
    db.refresh(insight)
    
    return InsightResponse(
        id=insight.id,
        comparison_id=insight.comparison_id,
        text=insight.text,
        confidence=insight.confidence or 1.0,
        created_at=insight.created_at.isoformat() if insight.created_at else ""
    )

