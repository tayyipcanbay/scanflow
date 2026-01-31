"""
AI insights generation service.
"""
import os
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class InsightsEngine:
    """Generates human-readable insights from mesh comparison data."""
    
    def __init__(self, use_llm: bool = False, llm_api_key: Optional[str] = None):
        """
        Initialize insights engine.
        
        Args:
            use_llm: Whether to use LLM for natural language generation
            llm_api_key: API key for LLM service (OpenAI/Anthropic)
        """
        self.use_llm = use_llm
        self.llm_api_key = llm_api_key or os.getenv("OPENAI_API_KEY")
    
    def generate_insights(
        self,
        comparison_stats: Dict[str, float],
        region_stats: Dict[str, Dict[str, float]],
        bia_data: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Generate insights from comparison data.
        
        Args:
            comparison_stats: Overall comparison statistics
            region_stats: Statistics per body region
            bia_data: Optional BIA metadata
            
        Returns:
            Dictionary with insights
        """
        # Rule-based analysis
        rule_based_insights = self._rule_based_analysis(
            comparison_stats, region_stats, bia_data
        )
        
        # LLM enhancement if enabled
        if self.use_llm and self.llm_api_key:
            try:
                enhanced_insights = self._llm_enhancement(rule_based_insights)
                return enhanced_insights
            except Exception as e:
                logger.warning(f"LLM enhancement failed: {e}, using rule-based only")
        
        return rule_based_insights
    
    def _rule_based_analysis(
        self,
        comparison_stats: Dict[str, float],
        region_stats: Dict[str, Dict[str, float]],
        bia_data: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Perform rule-based analysis.
        
        Args:
            comparison_stats: Overall statistics
            region_stats: Per-region statistics
            bia_data: Optional BIA data
            
        Returns:
            Dictionary with insights
        """
        insights_text = []
        confidence = 1.0
        
        # Overall change summary
        increase_pct = comparison_stats.get("increase_percentage", 0.0)
        decrease_pct = comparison_stats.get("decrease_percentage", 0.0)
        avg_magnitude = comparison_stats.get("avg_magnitude", 0.0)
        
        if decrease_pct > increase_pct and decrease_pct > 30:
            insights_text.append(
                f"Overall body volume shows reduction, with {decrease_pct:.1f}% of vertices "
                f"showing decrease. This suggests fat loss or volume reduction."
            )
        elif increase_pct > decrease_pct and increase_pct > 30:
            insights_text.append(
                f"Overall body volume shows increase, with {increase_pct:.1f}% of vertices "
                f"showing increase. This suggests muscle gain or volume increase."
            )
        else:
            insights_text.append(
                f"Body changes are mixed, with {increase_pct:.1f}% increase and "
                f"{decrease_pct:.1f}% decrease. This may indicate body recomposition."
            )
        
        # Region-specific insights
        region_insights = []
        for region_name, stats in region_stats.items():
            if stats["total_vertices"] == 0:
                continue
            
            region_display = region_name.replace("_", " ").title()
            increase_pct = stats.get("increase_percentage", 0.0)
            decrease_pct = stats.get("decrease_percentage", 0.0)
            avg_magnitude = stats.get("avg_magnitude", 0.0)
            
            if decrease_pct > 50 and avg_magnitude > 0.01:
                region_insights.append(
                    f"{region_display} region: Estimated ~{decrease_pct:.1f}% reduction, "
                    f"most change in this area."
                )
            elif increase_pct > 50 and avg_magnitude > 0.01:
                region_insights.append(
                    f"{region_display} region: Estimated ~{increase_pct:.1f}% increase, "
                    f"likely muscle gain."
                )
            elif abs(increase_pct - decrease_pct) < 20:
                region_insights.append(
                    f"{region_display} region: Mixed changes, moderate recomposition."
                )
        
        if region_insights:
            insights_text.extend(region_insights)
        
        # BIA context if available
        if bia_data:
            fat_pct = bia_data.get("fat_percentage")
            muscle_pct = bia_data.get("muscle_percentage")
            
            if fat_pct and muscle_pct:
                insights_text.append(
                    f"BIA data shows {fat_pct:.1f}% body fat and {muscle_pct:.1f}% muscle mass."
                )
        
        # Combine insights
        full_text = " ".join(insights_text)
        
        # Add disclaimer
        full_text += " Note: This is a visual estimation based on 3D mesh comparison, not a medical diagnosis."
        
        return {
            "text": full_text,
            "confidence": confidence,
            "source": "rule_based",
            "region_breakdown": region_stats
        }
    
    def _llm_enhancement(self, rule_based_data: Dict) -> Dict[str, any]:
        """
        Enhance insights using LLM.
        
        Args:
            rule_based_data: Rule-based analysis results
            
        Returns:
            Enhanced insights
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.llm_api_key)
            
            prompt = f"""
            You are a fitness and body composition analysis assistant. Based on the following 
            technical analysis of 3D body mesh comparison, generate a friendly, motivational, 
            and accurate summary.
            
            Technical Data:
            {rule_based_data['text']}
            
            Region Breakdown:
            {rule_based_data.get('region_breakdown', {})}
            
            Generate a concise, human-readable insight (2-3 sentences) that:
            1. Summarizes the key body changes
            2. Is motivational and positive
            3. Includes a disclaimer that this is visual estimation, not medical diagnosis
            4. Uses simple language that non-experts can understand
            
            Return only the insight text, no additional formatting.
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful fitness analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            enhanced_text = response.choices[0].message.content.strip()
            
            return {
                "text": enhanced_text,
                "confidence": rule_based_data["confidence"] * 0.9,  # Slightly lower confidence for LLM
                "source": "llm_enhanced",
                "region_breakdown": rule_based_data.get("region_breakdown", {})
            }
        except Exception as e:
            logger.error(f"LLM enhancement error: {e}")
            return rule_based_data

