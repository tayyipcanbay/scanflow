"""
Action plans API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from app.database.connection import get_db
from app.models.user import User
from app.models.comparison import MeshComparison, BIAData
from app.models.insights import ActionPlan
from app.services.action_planner import ActionPlanner

router = APIRouter()
action_planner = ActionPlanner()


class ActionPlanResponse(BaseModel):
    """Response model for action plans."""
    id: int
    user_id: int
    plan_type: str
    content: Dict[str, Any]
    is_active: bool
    created_at: str


@router.get("/{user_id}", response_model=List[ActionPlanResponse])
async def get_action_plans(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get action plans for a user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        List of action plans
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get latest comparison
    latest_comparison = db.query(MeshComparison).join(
        MeshComparison.comparison
    ).filter(
        MeshComparison.comparison.has(user_id=user_id)
    ).order_by(MeshComparison.created_at.desc()).first()
    
    if not latest_comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No comparison data available for user"
        )
    
    # Get existing plans
    existing_plans = db.query(ActionPlan).filter(
        ActionPlan.user_id == user_id,
        ActionPlan.is_active == True
    ).all()
    
    if existing_plans:
        return [
            ActionPlanResponse(
                id=plan.id,
                user_id=plan.user_id,
                plan_type=plan.plan_type,
                content=plan.content,
                is_active=plan.is_active,
                created_at=plan.created_at.isoformat() if plan.created_at else ""
            )
            for plan in existing_plans
        ]
    
    # Generate new plans
    displacement_data = latest_comparison.displacement_data
    region_stats = displacement_data.get("region_statistics", {})
    
    # Get BIA data
    bia_data = None
    bia_record = db.query(BIAData).filter(
        BIAData.mesh_upload_id == latest_comparison.comparison_id
    ).first()
    
    if bia_record:
        bia_data = {
            "fat_percentage": bia_record.fat_percentage,
            "muscle_percentage": bia_record.muscle_percentage,
        }
    
    # Generate meal plan
    meal_plan_data = action_planner.generate_meal_plan(
        region_stats,
        bia_data,
        country=user.country,
        preferences=None  # TODO: Add user preferences
    )
    
    meal_plan = ActionPlan(
        user_id=user_id,
        plan_type="meal",
        content=meal_plan_data,
        is_active=True
    )
    
    # Generate training plan
    training_plan_data = action_planner.generate_training_plan(
        region_stats,
        schedule=user.schedule_preferences
    )
    
    training_plan = ActionPlan(
        user_id=user_id,
        plan_type="training",
        content=training_plan_data,
        is_active=True
    )
    
    db.add(meal_plan)
    db.add(training_plan)
    db.commit()
    
    db.refresh(meal_plan)
    db.refresh(training_plan)
    
    return [
        ActionPlanResponse(
            id=meal_plan.id,
            user_id=meal_plan.user_id,
            plan_type=meal_plan.plan_type,
            content=meal_plan.content,
            is_active=meal_plan.is_active,
            created_at=meal_plan.created_at.isoformat() if meal_plan.created_at else ""
        ),
        ActionPlanResponse(
            id=training_plan.id,
            user_id=training_plan.user_id,
            plan_type=training_plan.plan_type,
            content=training_plan.content,
            is_active=training_plan.is_active,
            created_at=training_plan.created_at.isoformat() if training_plan.created_at else ""
        )
    ]

