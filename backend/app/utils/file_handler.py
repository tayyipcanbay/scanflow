"""
File handler for mesh file uploads, validation, and storage.
"""
import os
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
import shutil


class FileHandler:
    """Handles mesh file uploads and storage."""
    
    def __init__(self, storage_root: str = "backend/storage/meshes"):
        """
        Initialize file handler.
        
        Args:
            storage_root: Root directory for storing mesh files
        """
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
    
    def validate_mesh_file(self, file: UploadFile) -> bool:
        """
        Validate uploaded mesh file.
        
        Args:
            file: Uploaded file
            
        Returns:
            True if valid, False otherwise
        """
        # Check file extension
        allowed_extensions = {".glb", ".obj", ".fbx"}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return False
        
        # Check file size (max 100MB)
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > 100 * 1024 * 1024:  # 100MB
            return False
        
        return True
    
    async def save_mesh_file(
        self, 
        file: UploadFile, 
        user_id: int, 
        version: Optional[int] = None
    ) -> Path:
        """
        Save uploaded mesh file to storage.
        
        Args:
            file: Uploaded file
            user_id: User ID
            version: Optional version number
            
        Returns:
            Path to saved file
        """
        # Create user directory
        user_dir = self.storage_root / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        file_ext = Path(file.filename).suffix.lower()
        if version is not None:
            filename = f"mesh_v{version}{file_ext}"
        else:
            # Auto-increment version
            existing_files = list(user_dir.glob(f"mesh_v*{file_ext}"))
            if existing_files:
                versions = [
                    int(f.stem.split("_v")[1]) 
                    for f in existing_files 
                    if f.stem.startswith("mesh_v")
                ]
                version = max(versions) + 1 if versions else 1
            else:
                version = 1
            filename = f"mesh_v{version}{file_ext}"
        
        file_path = user_dir / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    def get_mesh_file_path(self, user_id: int, version: int) -> Optional[Path]:
        """
        Get path to mesh file for a specific user and version.
        
        Args:
            user_id: User ID
            version: Version number
            
        Returns:
            Path to file if exists, None otherwise
        """
        user_dir = self.storage_root / str(user_id)
        
        # Try different extensions
        for ext in [".glb", ".obj", ".fbx"]:
            file_path = user_dir / f"mesh_v{version}{ext}"
            if file_path.exists():
                return file_path
        
        return None
    
    def delete_mesh_file(self, user_id: int, version: int) -> bool:
        """
        Delete mesh file for a specific user and version.
        
        Args:
            user_id: User ID
            version: Version number
            
        Returns:
            True if deleted, False if not found
        """
        file_path = self.get_mesh_file_path(user_id, version)
        if file_path and file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def list_user_meshes(self, user_id: int) -> list[Path]:
        """
        List all mesh files for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of mesh file paths
        """
        user_dir = self.storage_root / str(user_id)
        if not user_dir.exists():
            return []
        
        mesh_files = []
        for ext in [".glb", ".obj", ".fbx"]:
            mesh_files.extend(user_dir.glob(f"mesh_v*{ext}"))
        
        return sorted(mesh_files, key=lambda p: int(p.stem.split("_v")[1]) if "_v" in p.stem else 0)

