"""
Utility functions for mesh operations.
"""
import numpy as np
from typing import Tuple
from scipy.spatial import cKDTree


def align_meshes(
    baseline_vertices: np.ndarray,
    comparison_vertices: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Align two meshes by centering them at origin.
    
    Args:
        baseline_vertices: Baseline mesh vertices
        comparison_vertices: Comparison mesh vertices
        
    Returns:
        Tuple of (aligned_baseline, aligned_comparison)
    """
    # Center both meshes at origin
    baseline_centroid = np.mean(baseline_vertices, axis=0)
    comparison_centroid = np.mean(comparison_vertices, axis=0)
    
    aligned_baseline = baseline_vertices - baseline_centroid
    aligned_comparison = comparison_vertices - comparison_centroid
    
    return aligned_baseline, aligned_comparison


def compute_vertex_correspondence(
    baseline_vertices: np.ndarray,
    comparison_vertices: np.ndarray
) -> np.ndarray:
    """
    Compute vertex correspondence between two meshes.
    Uses nearest neighbor matching if meshes have different vertex counts.
    
    Args:
        baseline_vertices: Baseline mesh vertices
        comparison_vertices: Comparison mesh vertices
        
    Returns:
        Array of corresponding vertex indices in comparison mesh for each baseline vertex
    """
    if len(baseline_vertices) == len(comparison_vertices):
        # If topology is identical, vertices correspond by index
        return np.arange(len(baseline_vertices))
    
    # Different vertex counts: use nearest neighbor matching
    # Build KDTree for efficient nearest neighbor search
    tree = cKDTree(comparison_vertices)
    
    # Find nearest neighbor in comparison mesh for each baseline vertex
    distances, indices = tree.query(baseline_vertices, k=1)
    
    return indices


def project_displacement_on_normal(
    displacement: np.ndarray,
    normal: np.ndarray
) -> float:
    """
    Project displacement vector onto surface normal.
    
    Args:
        displacement: Displacement vector
        normal: Surface normal vector
        
    Returns:
        Scalar projection (positive = outward, negative = inward)
    """
    return np.dot(displacement, normal)

