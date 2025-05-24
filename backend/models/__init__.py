from .user import User
from .org import Organisation, OrganisationUser
from .team import Team, TeamUser
from .invite import Invitation
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Cluster(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Fixed resources for the cluster
    total_cpu = Column(Float, nullable=False, default=0)
    total_ram = Column(Float, nullable=False, default=0)  # in GB
    total_gpu = Column(Float, nullable=False, default=0)

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    creator = relationship("User", back_populates="clusters")

    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    organization = relationship("Organization", back_populates="clusters")

    # Resources are tracked in a separate table
    resources = relationship("Resource", back_populates="cluster", uselist=False, cascade="all, delete-orphan")

    # Deployments in this cluster
    deployments = relationship("Deployment", back_populates="cluster")
