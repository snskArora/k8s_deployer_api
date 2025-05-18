from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    organisation_id: int


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TeamUserBase(BaseModel):
    role: str = "member"


class TeamUserCreate(TeamUserBase):
    user_id: int
    team_id: int


class TeamUser(TeamUserBase):
    id: int
    user_id: int
    team_id: int
    created_at: datetime

    class Config:
        orm_mode = True
