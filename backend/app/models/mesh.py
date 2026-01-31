"""
Mesh upload model.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base


class MeshUpload(Base):
    """Mesh upload model."""
    
    __tablename__ = "mesh_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    is_baseline = Column(Boolean, default=False, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", backref="mesh_uploads")
    
    # Unique constraint: one baseline per user
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

