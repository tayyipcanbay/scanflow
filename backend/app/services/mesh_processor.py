"""
Mesh processing service for loading and parsing 3D mesh files.
"""
import trimesh
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class MeshProcessor:
    """Processes 3D mesh files and extracts vertex data."""
    
    def __init__(self):
        """Initialize mesh processor."""
        self.supported_formats = {".glb", ".obj", ".fbx"}
    
    def load_mesh(self, file_path: Path) -> trimesh.Trimesh:
        """
        Load mesh from file.
        
        Args:
            file_path: Path to mesh file
            
        Returns:
            Trimesh object
            
        Raises:
            ValueError: If file format is not supported or file is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Mesh file not found: {file_path}")
        
        file_ext = file_path.suffix.lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        try:
            mesh = trimesh.load(str(file_path))
            
            # Handle scene objects (GLB files often contain scenes)
            if isinstance(mesh, trimesh.Scene):
                # Get the first geometry from the scene
                geometries = list(mesh.geometry.values())
                if not geometries:
                    raise ValueError("No geometry found in mesh file")
                mesh = geometries[0]
            
            # Ensure it's a Trimesh object
            if not isinstance(mesh, trimesh.Trimesh):
                raise ValueError(f"Loaded object is not a mesh: {type(mesh)}")
            
            return mesh
        except Exception as e:
            logger.error(f"Error loading mesh from {file_path}: {e}")
            raise ValueError(f"Failed to load mesh: {e}")
    
    def normalize_mesh(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """
        Normalize mesh topology and ensure consistent vertex ordering.
        
        Args:
            mesh: Input mesh
            
        Returns:
            Normalized mesh
        """
        # Remove duplicate vertices
        mesh.merge_vertices()
        
        # Remove unused vertices
        mesh.remove_unreferenced_vertices()
        
        # Ensure consistent face winding
        mesh.fix_normals()
        
        # Center mesh at origin (optional, but helpful for comparison)
        # mesh.vertices -= mesh.centroid
        
        return mesh
    
    def extract_vertex_data(
        self, 
        mesh: trimesh.Trimesh
    ) -> Dict[str, np.ndarray]:
        """
        Extract vertex positions, normals, and faces from mesh.
        
        Args:
            mesh: Trimesh object
            
        Returns:
            Dictionary with 'vertices', 'normals', and 'faces'
        """
        vertices = np.array(mesh.vertices, dtype=np.float32)
        faces = np.array(mesh.faces, dtype=np.int32)
        
        # Compute vertex normals if not present
        if hasattr(mesh, "vertex_normals") and mesh.vertex_normals is not None:
            normals = np.array(mesh.vertex_normals, dtype=np.float32)
        else:
            # Compute normals from faces
            normals = self._compute_vertex_normals(vertices, faces)
        
        return {
            "vertices": vertices,
            "normals": normals,
            "faces": faces,
            "vertex_count": len(vertices),
            "face_count": len(faces)
        }
    
    def _compute_vertex_normals(
        self, 
        vertices: np.ndarray, 
        faces: np.ndarray
    ) -> np.ndarray:
        """
        Compute vertex normals from faces.
        
        Args:
            vertices: Vertex positions
            faces: Face indices
            
        Returns:
            Vertex normals
        """
        normals = np.zeros_like(vertices)
        
        # Compute face normals
        for face in faces:
            v0, v1, v2 = vertices[face]
            face_normal = np.cross(v1 - v0, v2 - v0)
            face_normal = face_normal / (np.linalg.norm(face_normal) + 1e-8)
            
            # Add to vertex normals
            normals[face] += face_normal
        
        # Normalize
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        norms[norms < 1e-8] = 1.0
        normals = normals / norms
        
        return normals
    
    def validate_mesh_structure(self, mesh: trimesh.Trimesh) -> Tuple[bool, Optional[str]]:
        """
        Validate mesh structure and topology consistency.
        
        Args:
            mesh: Trimesh object to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(mesh.vertices) == 0:
            return False, "Mesh has no vertices"
        
        if len(mesh.faces) == 0:
            return False, "Mesh has no faces"
        
        # Check for valid face indices
        max_vertex_idx = len(mesh.vertices) - 1
        if np.any(mesh.faces > max_vertex_idx) or np.any(mesh.faces < 0):
            return False, "Invalid face indices"
        
        # Check for degenerate faces
        face_areas = mesh.area_faces
        if np.any(face_areas < 1e-10):
            return False, "Mesh contains degenerate faces"
        
        return True, None
    
    def process_mesh_file(
        self, 
        file_path: Path
    ) -> Dict[str, np.ndarray]:
        """
        Complete mesh processing pipeline: load, normalize, extract data.
        
        Args:
            file_path: Path to mesh file
            
        Returns:
            Dictionary with processed mesh data
        """
        # Load mesh
        mesh = self.load_mesh(file_path)
        
        # Validate structure
        is_valid, error_msg = self.validate_mesh_structure(mesh)
        if not is_valid:
            raise ValueError(f"Invalid mesh structure: {error_msg}")
        
        # Normalize
        mesh = self.normalize_mesh(mesh)
        
        # Extract data
        vertex_data = self.extract_vertex_data(mesh)
        
        return vertex_data
    
    def compare_topology(
        self, 
        mesh1_data: Dict[str, np.ndarray], 
        mesh2_data: Dict[str, np.ndarray]
    ) -> Tuple[bool, Optional[str]]:
        """
        Compare topology of two meshes to ensure they can be compared.
        
        Args:
            mesh1_data: First mesh data
            mesh2_data: Second mesh data
            
        Returns:
            Tuple of (topology_match, error_message)
        """
        if mesh1_data["vertex_count"] != mesh2_data["vertex_count"]:
            return False, f"Vertex count mismatch: {mesh1_data['vertex_count']} vs {mesh2_data['vertex_count']}"
        
        if mesh1_data["face_count"] != mesh2_data["face_count"]:
            return False, f"Face count mismatch: {mesh1_data['face_count']} vs {mesh2_data['face_count']}"
        
        # Check if faces are identical (same topology)
        if not np.array_equal(mesh1_data["faces"], mesh2_data["faces"]):
            return False, "Face topology mismatch"
        
        return True, None

