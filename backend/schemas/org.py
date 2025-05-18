from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrganisationBase(BaseModel):
    name: str
    description: Optional[str] = None


class OrganisationCreate(OrganisationBase):
    pass


class Organisation(OrganisationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class OrganisationUserBase(BaseModel):
    role: str = "member"


class OrganisationUserCreate(OrganisationUserBase):
    user_id: int
    organisation_id: int


class OrganisationUser(OrganisationUserBase):
    id: int
    user_id: int
    organisation_id: int
    created_at: datetime

    class Config:
        orm_mode = True
