from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class InvitationBase(BaseModel):
    email: EmailStr
    organisation_id: int
    team_id: Optional[int] = None


class InvitationCreate(InvitationBase):
    expires_at: Optional[datetime] = None


class Invitation(InvitationBase):
    id: int
    invite_code: str
    created_by: int
    is_valid: bool
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True


class InvitationAccept(BaseModel):
    user_id: int
