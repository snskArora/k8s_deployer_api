from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organisation_users = relationship("OrganisationUser", back_populates="organisation")
    teams = relationship("Team", back_populates="organisation")
    invitations = relationship("Invitation", back_populates="organisation")


class OrganisationUser(Base):
    __tablename__ = "organisation_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    role = Column(String, default="member")  # e.g., "admin", "member"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="organisation_users")
    organisation = relationship("Organisation", back_populates="organisation_users")
