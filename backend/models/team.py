from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organisation = relationship("Organisation", back_populates="teams")
    team_users = relationship("TeamUser", back_populates="team")
    invitations = relationship("Invitation", back_populates="team")


class TeamUser(Base):
    __tablename__ = "team_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    role = Column(String, default="member")  # e.g., "admin", "member"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="team_users")
    team = relationship("Team", back_populates="team_users")
