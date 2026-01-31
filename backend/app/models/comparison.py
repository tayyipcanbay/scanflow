"""
Comparison result model.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base


class MeshComparison(Base):
    """Mesh comparison result model."""
    
    __tablename__ = "mesh_comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    baseline_id = Column(Integer, ForeignKey("mesh_uploads.id"), nullable=False)
    comparison_id = Column(Integer, ForeignKey("mesh_uploads.id"), nullable=False)
    
    # Displacement data stored as JSON
    # Contains: displacements, magnitudes, projections, directions
    displacement_data = Column(JSON, nullable=False)
    
    # Statistics
    avg_magnitude = Column(Float, nullable=True)
    max_magnitude = Column(Float, nullable=True)
    increase_percentage = Column(Float, nullable=True)
    decrease_percentage = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    baseline = relationship("MeshUpload", foreign_keys=[baseline_id], backref="baseline_comparisons")
    comparison = relationship("MeshUpload", foreign_keys=[comparison_id], backref="comparison_comparisons")


class BIAData(Base):
    """BIA (Bioelectrical Impedance Analysis) data model."""
    
    __tablename__ = "bia_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mesh_upload_id = Column(Integer, ForeignKey("mesh_uploads.id"), nullable=True)
    
    weight = Column(Float, nullable=True)  # kg
    bmi = Column(Float, nullable=True)
    fat_percentage = Column(Float, nullable=True)  # %
    muscle_percentage = Column(Float, nullable=True)  # %
    water_percentage = Column(Float, nullable=True)  # %
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", backref="bia_data")
    mesh_upload = relationship("MeshUpload", backref="bia_data")

