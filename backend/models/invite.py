import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


def generate_invite_code():
    return str(uuid.uuid4())


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    invite_code = Column(String, unique=True, index=True, default=generate_invite_code)
    email = Column(String, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    is_valid = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    organisation = relationship("Organisation", back_populates="invitations")
    team = relationship("Team", back_populates="invitations")
    # team = relationship("Team", back_populates="invitations", nullable=True)
    creator = relationship("User", foreign_keys=[created_by])
