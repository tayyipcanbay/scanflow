"""
Color mapping service for visualizing mesh changes.
"""
import numpy as np
from typing import Dict, Tuple, Optional


class ColorMapper:
    """Maps displacement values to colors for visualization."""
    
    def __init__(
        self,
        change_threshold: float = 0.001,
        max_change: Optional[float] = None
    ):
        """
        Initialize color mapper.
        
        Args:
            change_threshold: Minimum change magnitude to be considered significant
            max_change: Maximum change magnitude for normalization (None = auto)
        """
        self.change_threshold = change_threshold
        self.max_change = max_change
    
    def map_displacement_to_color(
        self,
        projections: np.ndarray,
        magnitudes: np.ndarray,
        normalize: bool = True
    ) -> np.ndarray:
        """
        Map displacement projections to RGB colors.
        
        Color scheme:
        - Green (0, 255, 0) → strong decrease
        - White (255, 255, 255) → no change
        - Red (255, 0, 0) → strong increase
        
        Args:
            projections: Projection of displacement onto surface normal
            magnitudes: Magnitude of displacement
            normalize: Whether to normalize based on max change
            
        Returns:
            Array of RGB colors (N x 3, values 0-255)
        """
        colors = np.zeros((len(projections), 3), dtype=np.uint8)
        
        # Determine max change for normalization
        if normalize and self.max_change is None:
            max_abs_projection = np.max(np.abs(projections))
            if max_abs_projection > 0:
                max_change = max_abs_projection
            else:
                max_change = 1.0
        elif normalize:
            max_change = self.max_change
        else:
            max_change = 1.0
        
        # Normalize projections to [-1, 1] range
        if max_change > 0:
            normalized = np.clip(projections / max_change, -1.0, 1.0)
        else:
            normalized = np.zeros_like(projections)
        
        # Map to colors
        for i, (proj, mag) in enumerate(zip(normalized, magnitudes)):
            if abs(proj) < self.change_threshold / max_change if max_change > 0 else self.change_threshold:
                # No significant change - white
                colors[i] = [255, 255, 255]
            elif proj < 0:
                # Decrease - green gradient
                intensity = min(abs(proj), 1.0)
                green_value = int(255 * intensity)
                colors[i] = [0, green_value, 0]
            else:
                # Increase - red gradient
                intensity = min(proj, 1.0)
                red_value = int(255 * intensity)
                colors[i] = [red_value, 0, 0]
        
        return colors
    
    def map_displacement_to_colors_normalized(
        self,
        projections: np.ndarray,
        magnitudes: np.ndarray
    ) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Map displacement to colors with automatic normalization and return metadata.
        
        Args:
            projections: Projection of displacement onto surface normal
            magnitudes: Magnitude of displacement
            
        Returns:
            Tuple of (colors, metadata)
        """
        # Compute normalization parameters
        max_abs_projection = float(np.max(np.abs(projections))) if len(projections) > 0 else 1.0
        if max_abs_projection == 0:
            max_abs_projection = 1.0
        
        # Create mapper with computed max_change
        mapper = ColorMapper(
            change_threshold=self.change_threshold,
            max_change=max_abs_projection
        )
        
        colors = mapper.map_displacement_to_color(projections, magnitudes, normalize=True)
        
        metadata = {
            "max_change": max_abs_projection,
            "change_threshold": self.change_threshold,
            "color_scheme": "green_decrease_red_increase"
        }
        
        return colors, metadata
    
    def get_color_legend(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Get color legend for visualization.
        
        Returns:
            Dictionary mapping description to RGB color
        """
        return {
            "strong_decrease": (0, 255, 0),  # Green
            "moderate_decrease": (128, 255, 128),  # Light green
            "no_change": (255, 255, 255),  # White
            "moderate_increase": (255, 128, 128),  # Light red
            "strong_increase": (255, 0, 0),  # Red
        }
    
    def export_color_data(
        self,
        colors: np.ndarray,
        vertices: np.ndarray
    ) -> Dict:
        """
        Export color data in format suitable for frontend consumption.
        
        Args:
            colors: RGB color array (N x 3)
            vertices: Vertex positions (N x 3)
            
        Returns:
            Dictionary with color data
        """
        return {
            "colors": colors.tolist(),
            "vertices": vertices.tolist(),
            "color_format": "rgb",
            "color_range": [0, 255]
        }

