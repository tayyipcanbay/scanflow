"""
Region detection service for mapping vertices to body regions.
"""
import numpy as np
from typing import Dict, List, Tuple
from enum import Enum


class BodyRegion(Enum):
    """Body region enumeration."""
    WAIST = "waist"
    CHEST = "chest"
    ARMS = "arms"
    THIGHS = "thighs"
    HIPS = "hips"
    OTHER = "other"


class RegionDetector:
    """Detects and maps vertices to body regions."""
    
    def __init__(self):
        """Initialize region detector with default region definitions."""
        # These are approximate ranges - may need adjustment based on mesh coordinate system
        # Assumes Y is vertical (up), X is left-right, Z is front-back
        self.region_definitions = {
            BodyRegion.WAIST: {
                "y_range": (-0.3, 0.1),  # Vertical range
                "x_bounds": (-0.5, 0.5),  # Horizontal bounds
                "z_bounds": (-0.5, 0.5),  # Depth bounds
            },
            BodyRegion.CHEST: {
                "y_range": (0.1, 0.5),
                "x_bounds": (-0.5, 0.5),
                "z_bounds": (-0.5, 0.5),
            },
            BodyRegion.ARMS: {
                "x_extreme": 0.3,  # X coordinate far from center
                "y_range": (-0.2, 0.4),
            },
            BodyRegion.THIGHS: {
                "y_range": (-0.8, -0.3),
                "x_bounds": (-0.4, 0.4),
                "z_bounds": (-0.5, 0.5),
            },
            BodyRegion.HIPS: {
                "y_range": (-0.3, 0.0),
                "x_bounds": (-0.5, 0.5),
                "z_bounds": (-0.5, 0.5),
            },
        }
    
    def detect_regions(
        self, 
        vertices: np.ndarray,
        normalize: bool = True
    ) -> Dict[BodyRegion, np.ndarray]:
        """
        Detect body regions from vertex positions.
        
        Args:
            vertices: Vertex positions (N x 3)
            normalize: Whether to normalize coordinates first
            
        Returns:
            Dictionary mapping region to boolean mask of vertices
        """
        if normalize:
            # Normalize to center at origin
            centroid = np.mean(vertices, axis=0)
            vertices = vertices - centroid
            
            # Normalize scale (optional - helps with different mesh scales)
            max_range = np.max(np.abs(vertices))
            if max_range > 0:
                vertices = vertices / max_range
        
        region_masks = {}
        
        # Waist region
        waist_def = self.region_definitions[BodyRegion.WAIST]
        waist_mask = (
            (vertices[:, 1] >= waist_def["y_range"][0]) &
            (vertices[:, 1] <= waist_def["y_range"][1]) &
            (vertices[:, 0] >= waist_def["x_bounds"][0]) &
            (vertices[:, 0] <= waist_def["x_bounds"][1]) &
            (vertices[:, 2] >= waist_def["z_bounds"][0]) &
            (vertices[:, 2] <= waist_def["z_bounds"][1])
        )
        region_masks[BodyRegion.WAIST] = waist_mask
        
        # Chest region
        chest_def = self.region_definitions[BodyRegion.CHEST]
        chest_mask = (
            (vertices[:, 1] >= chest_def["y_range"][0]) &
            (vertices[:, 1] <= chest_def["y_range"][1]) &
            (vertices[:, 0] >= chest_def["x_bounds"][0]) &
            (vertices[:, 0] <= chest_def["x_bounds"][1]) &
            (vertices[:, 2] >= chest_def["z_bounds"][0]) &
            (vertices[:, 2] <= chest_def["z_bounds"][1])
        )
        region_masks[BodyRegion.CHEST] = chest_mask
        
        # Arms region (X-axis extremes)
        arms_def = self.region_definitions[BodyRegion.ARMS]
        arms_mask = (
            (np.abs(vertices[:, 0]) >= arms_def["x_extreme"]) &
            (vertices[:, 1] >= arms_def["y_range"][0]) &
            (vertices[:, 1] <= arms_def["y_range"][1])
        )
        region_masks[BodyRegion.ARMS] = arms_mask
        
        # Thighs region
        thighs_def = self.region_definitions[BodyRegion.THIGHS]
        thighs_mask = (
            (vertices[:, 1] >= thighs_def["y_range"][0]) &
            (vertices[:, 1] <= thighs_def["y_range"][1]) &
            (vertices[:, 0] >= thighs_def["x_bounds"][0]) &
            (vertices[:, 0] <= thighs_def["x_bounds"][1]) &
            (vertices[:, 2] >= thighs_def["z_bounds"][0]) &
            (vertices[:, 2] <= thighs_def["z_bounds"][1])
        )
        region_masks[BodyRegion.THIGHS] = thighs_mask
        
        # Hips region
        hips_def = self.region_definitions[BodyRegion.HIPS]
        hips_mask = (
            (vertices[:, 1] >= hips_def["y_range"][0]) &
            (vertices[:, 1] <= hips_def["y_range"][1]) &
            (vertices[:, 0] >= hips_def["x_bounds"][0]) &
            (vertices[:, 0] <= hips_def["x_bounds"][1]) &
            (vertices[:, 2] >= hips_def["z_bounds"][0]) &
            (vertices[:, 2] <= hips_def["z_bounds"][1])
        )
        region_masks[BodyRegion.HIPS] = hips_mask
        
        # Other region (vertices not in any specific region)
        all_regions_mask = (
            waist_mask | chest_mask | arms_mask | thighs_mask | hips_mask
        )
        region_masks[BodyRegion.OTHER] = ~all_regions_mask
        
        return region_masks
    
    def map_vertices_to_regions(
        self, 
        vertices: np.ndarray
    ) -> np.ndarray:
        """
        Map each vertex to its primary region.
        
        Args:
            vertices: Vertex positions (N x 3)
            
        Returns:
            Array of region names for each vertex
        """
        region_masks = self.detect_regions(vertices)
        
        # Create mapping (priority order if overlap)
        region_order = [
            BodyRegion.ARMS,
            BodyRegion.CHEST,
            BodyRegion.WAIST,
            BodyRegion.HIPS,
            BodyRegion.THIGHS,
            BodyRegion.OTHER,
        ]
        
        vertex_regions = np.full(len(vertices), BodyRegion.OTHER.value, dtype=object)
        
        for region in region_order:
            mask = region_masks[region]
            vertex_regions[mask] = region.value
        
        return vertex_regions
    
    def aggregate_region_statistics(
        self,
        vertices: np.ndarray,
        displacements: np.ndarray,
        magnitudes: np.ndarray,
        projections: np.ndarray
    ) -> Dict[str, Dict[str, float]]:
        """
        Aggregate statistics per body region.
        
        Args:
            vertices: Vertex positions
            displacements: Displacement vectors
            magnitudes: Magnitude of displacement
            projections: Projection of displacement onto normal
            
        Returns:
            Dictionary with statistics per region
        """
        region_masks = self.detect_regions(vertices)
        region_stats = {}
        
        for region, mask in region_masks.items():
            if not np.any(mask):
                continue
            
            region_magnitudes = magnitudes[mask]
            region_projections = projections[mask]
            
            # Count increases and decreases
            increase_mask = region_projections > 0
            decrease_mask = region_projections < 0
            
            increase_count = int(np.sum(increase_mask))
            decrease_count = int(np.sum(decrease_mask))
            total_vertices = int(np.sum(mask))
            
            region_stats[region.value] = {
                "total_vertices": total_vertices,
                "avg_magnitude": float(np.mean(region_magnitudes)),
                "max_magnitude": float(np.max(region_magnitudes)),
                "min_magnitude": float(np.min(region_magnitudes)),
                "increase_count": increase_count,
                "decrease_count": decrease_count,
                "increase_percentage": (increase_count / total_vertices * 100) if total_vertices > 0 else 0.0,
                "decrease_percentage": (decrease_count / total_vertices * 100) if total_vertices > 0 else 0.0,
                "avg_increase": float(np.mean(region_projections[increase_mask])) if increase_count > 0 else 0.0,
                "avg_decrease": float(np.mean(region_projections[decrease_mask])) if decrease_count > 0 else 0.0,
            }
        
        return region_stats

