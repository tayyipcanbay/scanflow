"""
Action planner service for generating meal and training plans.
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ActionPlanner:
    """Generates personalized meal and training plans."""
    
    def __init__(self):
        """Initialize action planner."""
        # Country-specific food preferences (simplified)
        self.food_preferences = {
            "US": ["chicken", "salmon", "rice", "broccoli", "eggs", "oatmeal"],
            "IN": ["dal", "roti", "rice", "vegetables", "yogurt", "paneer"],
            "CN": ["tofu", "rice", "vegetables", "fish", "eggs", "noodles"],
            "JP": ["salmon", "rice", "miso soup", "vegetables", "tofu", "eggs"],
            "default": ["chicken", "rice", "vegetables", "eggs", "fish", "fruits"],
        }
    
    def generate_meal_plan(
        self,
        region_stats: Dict[str, Dict[str, float]],
        bia_data: Optional[Dict] = None,
        country: Optional[str] = None,
        preferences: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate personalized meal plan.
        
        Args:
            region_stats: Statistics per body region
            bia_data: Optional BIA metadata
            country: User's country for food preferences
            preferences: User's food preferences
            
        Returns:
            Dictionary with meal plan
        """
        # Determine goal based on changes
        goal = self._determine_goal(region_stats, bia_data)
        
        # Get food list
        foods = self._get_food_list(country, preferences)
        
        # Generate plan based on goal
        if goal == "fat_loss":
            plan = self._fat_loss_meal_plan(foods)
        elif goal == "muscle_gain":
            plan = self._muscle_gain_meal_plan(foods)
        else:
            plan = self._recomposition_meal_plan(foods)
        
        return {
            "type": "meal",
            "goal": goal,
            "plan": plan,
            "duration_weeks": 4,
            "notes": "Adjust portions based on your activity level and consult a nutritionist for personalized advice."
        }
    
    def generate_training_plan(
        self,
        region_stats: Dict[str, Dict[str, float]],
        schedule: Optional[Dict] = None
    ) -> Dict:
        """
        Generate personalized training plan.
        
        Args:
            region_stats: Statistics per body region
            schedule: User schedule constraints (days_per_week, time_per_session)
            
        Returns:
            Dictionary with training plan
        """
        # Identify focus areas
        focus_areas = self._identify_focus_areas(region_stats)
        
        # Get schedule constraints
        days_per_week = schedule.get("days_per_week", 3) if schedule else 3
        time_per_session = schedule.get("time_per_session", 60) if schedule else 60  # minutes
        
        # Generate plan
        plan = self._create_training_schedule(focus_areas, days_per_week, time_per_session)
        
        return {
            "type": "training",
            "focus_areas": focus_areas,
            "schedule": plan,
            "days_per_week": days_per_week,
            "time_per_session": time_per_session,
            "notes": "Progressive overload: gradually increase weight or reps each week."
        }
    
    def _determine_goal(
        self,
        region_stats: Dict[str, Dict[str, float]],
        bia_data: Optional[Dict] = None
    ) -> str:
        """Determine primary goal from changes."""
        total_increase = sum(
            stats.get("increase_percentage", 0) for stats in region_stats.values()
        )
        total_decrease = sum(
            stats.get("decrease_percentage", 0) for stats in region_stats.values()
        )
        
        if total_decrease > total_increase * 1.5:
            return "fat_loss"
        elif total_increase > total_decrease * 1.5:
            return "muscle_gain"
        else:
            return "recomposition"
    
    def _get_food_list(
        self,
        country: Optional[str],
        preferences: Optional[List[str]]
    ) -> List[str]:
        """Get food list based on country and preferences."""
        if preferences:
            return preferences
        
        if country and country.upper() in self.food_preferences:
            return self.food_preferences[country.upper()]
        
        return self.food_preferences["default"]
    
    def _fat_loss_meal_plan(self, foods: List[str]) -> Dict:
        """Generate fat loss meal plan."""
        return {
            "breakfast": f"{foods[0]} with vegetables, portion: 200g",
            "lunch": f"{foods[1]} with {foods[2]}, portion: 250g",
            "dinner": f"{foods[3]} with salad, portion: 200g",
            "snacks": "Fruits, nuts (moderate portions)",
            "calories": "Target: 500-700 calorie deficit",
            "macros": "High protein (30%), Moderate carbs (40%), Low fat (30%)"
        }
    
    def _muscle_gain_meal_plan(self, foods: List[str]) -> Dict:
        """Generate muscle gain meal plan."""
        return {
            "breakfast": f"{foods[0]} with {foods[2]}, portion: 250g",
            "lunch": f"{foods[1]} with {foods[2]}, portion: 300g",
            "dinner": f"{foods[0]} with vegetables, portion: 250g",
            "post_workout": f"{foods[4]} or protein shake",
            "snacks": "Nuts, yogurt, fruits",
            "calories": "Target: 300-500 calorie surplus",
            "macros": "High protein (35%), High carbs (45%), Moderate fat (20%)"
        }
    
    def _recomposition_meal_plan(self, foods: List[str]) -> Dict:
        """Generate recomposition meal plan."""
        return {
            "breakfast": f"{foods[0]} with vegetables, portion: 200g",
            "lunch": f"{foods[1]} with {foods[2]}, portion: 250g",
            "dinner": f"{foods[3]} with salad, portion: 200g",
            "snacks": "Protein-rich snacks, fruits",
            "calories": "Target: Maintenance calories",
            "macros": "High protein (35%), Moderate carbs (40%), Moderate fat (25%)"
        }
    
    def _identify_focus_areas(
        self,
        region_stats: Dict[str, Dict[str, float]]
    ) -> List[str]:
        """Identify body regions that need focus."""
        focus_areas = []
        
        for region, stats in region_stats.items():
            if stats.get("total_vertices", 0) == 0:
                continue
            
            # If region shows decrease and user wants to maintain/gain
            # Or if region shows increase and user wants to continue
            avg_magnitude = stats.get("avg_magnitude", 0.0)
            if avg_magnitude > 0.01:  # Significant change
                focus_areas.append(region.replace("_", " ").title())
        
        if not focus_areas:
            focus_areas = ["Full Body"]  # Default
        
        return focus_areas[:3]  # Top 3 focus areas
    
    def _create_training_schedule(
        self,
        focus_areas: List[str],
        days_per_week: int,
        time_per_session: int
    ) -> Dict:
        """Create training schedule."""
        if days_per_week == 3:
            return {
                "day_1": f"Upper body focus: {focus_areas[0] if focus_areas else 'Chest & Back'}",
                "day_2": "Rest or light cardio",
                "day_3": f"Lower body focus: {focus_areas[1] if len(focus_areas) > 1 else 'Legs'}",
                "day_4": "Rest or light cardio",
                "day_5": f"Full body or {focus_areas[2] if len(focus_areas) > 2 else 'Core'}",
                "day_6": "Rest",
                "day_7": "Rest or active recovery"
            }
        elif days_per_week == 4:
            return {
                "day_1": f"Upper body: {focus_areas[0] if focus_areas else 'Push'}",
                "day_2": f"Lower body: {focus_areas[1] if len(focus_areas) > 1 else 'Legs'}",
                "day_3": "Rest",
                "day_4": f"Upper body: {focus_areas[0] if focus_areas else 'Pull'}",
                "day_5": f"Lower body: {focus_areas[1] if len(focus_areas) > 1 else 'Legs'}",
                "day_6": "Rest",
                "day_7": "Rest or active recovery"
            }
        else:
            # 5+ days
            return {
                "day_1": f"Push: {focus_areas[0] if focus_areas else 'Chest & Shoulders'}",
                "day_2": f"Pull: {focus_areas[1] if len(focus_areas) > 1 else 'Back & Arms'}",
                "day_3": f"Legs: {focus_areas[2] if len(focus_areas) > 2 else 'Lower Body'}",
                "day_4": f"Push: {focus_areas[0] if focus_areas else 'Chest & Shoulders'}",
                "day_5": f"Pull: {focus_areas[1] if len(focus_areas) > 1 else 'Back & Arms'}",
                "day_6": "Legs or Rest",
                "day_7": "Rest or active recovery"
            }

