"""
Mesh comparison service for computing geometric differences between meshes.
"""
import numpy as np
from typing import Dict, Optional
import logging

from app.services.mesh_processor import MeshProcessor
from app.utils.mesh_utils import align_meshes, compute_vertex_correspondence, project_displacement_on_normal

logger = logging.getLogger(__name__)


class MeshComparator:
    """Compares meshes and computes displacement maps."""
    
    def __init__(self):
        """Initialize mesh comparator."""
        self.mesh_processor = MeshProcessor()
    
    def compare_meshes(
        self,
        baseline_data: Dict[str, np.ndarray],
        comparison_data: Dict[str, np.ndarray],
        align: bool = True
    ) -> Dict[str, np.ndarray]:
        """
        Compare two meshes and compute displacement map.
        
        Args:
            baseline_data: Baseline mesh data (from mesh_processor)
            comparison_data: Comparison mesh data (from mesh_processor)
            align: Whether to align meshes before comparison
            
        Returns:
            Dictionary with displacement data:
            - displacements: Displacement vectors for each vertex
            - magnitudes: Magnitude of displacement for each vertex
            - projections: Projection of displacement onto surface normal
            - directions: Direction of change (1 for increase, -1 for decrease)
        """
        baseline_vertices = baseline_data["vertices"]
        comparison_vertices = comparison_data["vertices"]
        baseline_normals = baseline_data["normals"]
        
        # Align meshes if requested
        if align:
            baseline_vertices, comparison_vertices = align_meshes(
                baseline_vertices, comparison_vertices
            )
        
        # Compute vertex correspondence (handles different vertex counts)
        correspondence = compute_vertex_correspondence(
            baseline_vertices, comparison_vertices
        )
        
        # Get corresponding vertices from comparison mesh
        # If meshes have same count, correspondence is identity mapping
        # If different, correspondence contains nearest neighbor indices
        corresponding_comparison_vertices = comparison_vertices[correspondence]
        
        # Compute displacement vectors
        displacements = corresponding_comparison_vertices - baseline_vertices
        
        # Compute magnitude of displacement
        magnitudes = np.linalg.norm(displacements, axis=1)
        
        # Project displacement onto surface normals
        projections = np.array([
            project_displacement_on_normal(displacements[i], baseline_normals[i])
            for i in range(len(displacements))
        ])
        
        # Determine direction: positive = outward (increase/red), negative = inward (decrease/green)
        directions = np.sign(projections)
        
        return {
            "displacements": displacements,
            "magnitudes": magnitudes,
            "projections": projections,
            "directions": directions,
            "baseline_vertices": baseline_vertices,
            "comparison_vertices": corresponding_comparison_vertices,  # Use corresponding vertices
            "baseline_normals": baseline_normals
        }
    
    def compare_mesh_files(
        self,
        baseline_path: str,
        comparison_path: str,
        align: bool = True
    ) -> Dict[str, np.ndarray]:
        """
        Compare two mesh files and compute displacement map.
        
        Args:
            baseline_path: Path to baseline mesh file
            comparison_path: Path to comparison mesh file
            align: Whether to align meshes before comparison
            
        Returns:
            Dictionary with displacement data
        """
        # Process both meshes
        baseline_data = self.mesh_processor.process_mesh_file(baseline_path)
        comparison_data = self.mesh_processor.process_mesh_file(comparison_path)
        
        # Validate topology compatibility
        topology_match, error_msg = self.mesh_processor.compare_topology(
            baseline_data, comparison_data
        )
        if not topology_match:
            raise ValueError(f"Topology mismatch: {error_msg}")
        
        # Compare meshes
        return self.compare_meshes(baseline_data, comparison_data, align=align)
    
    def get_displacement_statistics(
        self,
        comparison_result: Dict[str, np.ndarray]
    ) -> Dict[str, float]:
        """
        Compute statistics from comparison result.
        
        Args:
            comparison_result: Result from compare_meshes
            
        Returns:
            Dictionary with statistics
        """
        magnitudes = comparison_result["magnitudes"]
        projections = comparison_result["projections"]
        directions = comparison_result["directions"]
        
        # Overall statistics
        avg_magnitude = float(np.mean(magnitudes))
        max_magnitude = float(np.max(magnitudes))
        min_magnitude = float(np.min(magnitudes))
        
        # Direction-based statistics
        increase_mask = directions > 0
        decrease_mask = directions < 0
        no_change_mask = directions == 0
        
        increase_count = int(np.sum(increase_mask))
        decrease_count = int(np.sum(decrease_mask))
        no_change_count = int(np.sum(no_change_mask))
        total_vertices = len(magnitudes)
        
        # Average change by direction
        avg_increase = float(np.mean(projections[increase_mask])) if increase_count > 0 else 0.0
        avg_decrease = float(np.mean(projections[decrease_mask])) if decrease_count > 0 else 0.0
        
        return {
            "avg_magnitude": avg_magnitude,
            "max_magnitude": max_magnitude,
            "min_magnitude": min_magnitude,
            "increase_count": increase_count,
            "decrease_count": decrease_count,
            "no_change_count": no_change_count,
            "increase_percentage": (increase_count / total_vertices) * 100 if total_vertices > 0 else 0.0,
            "decrease_percentage": (decrease_count / total_vertices) * 100 if total_vertices > 0 else 0.0,
            "avg_increase": avg_increase,
            "avg_decrease": avg_decrease,
            "total_vertices": total_vertices
        }

