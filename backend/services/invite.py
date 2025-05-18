from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.invite import Invitation
from ..models.org import Organisation, OrganisationUser
from ..models.team import Team, TeamUser
from ..models.user import User


def create_invitation(db: Session, organisation_id: int, email: str, created_by: int, team_id: int | None = None, expires_at: datetime | None = None):
    # Check if organisation exists
    organisation = db.query(Organisation).filter(Organisation.id == organisation_id).first()
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")

    # Check if team exists if team_id is provided
    if team_id:
        team = db.query(Team).filter(Team.id == team_id, Team.organisation_id == organisation_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found or not part of the organisation")

    creator = db.query(OrganisationUser).filter(OrganisationUser.organisation_id == organisation_id, OrganisationUser.user_id == created_by).first()
    if not creator:
        raise HTTPException(status_code=404, detail="User not found in the Organization")
    creator_role = creator.role
    if creator_role not in ["admin", "maintainer"]:
        raise HTTPException(status_code=401, detail=f"User should be admin or maintainer but is {creator_role}")

    invite_code = str(uuid.uuid4())
    if expires_at is None:
        expires_at = datetime.now(timezone.utc) + timedelta(days=3)

    invitation = Invitation(
        invite_code=invite_code,
        email=email,
        organisation_id=organisation_id,
        team_id=team_id,
        created_by=created_by,
        expires_at=expires_at
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


def get_invitation_by_code(db: Session, invite_code: str):
    invitation = db.query(Invitation).filter(Invitation.invite_code == invite_code).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    # Check if invitation is expired
    if invitation.expires_at < datetime.now(timezone.utc):
        invitation.is_valid = False
        db.commit()
        raise HTTPException(status_code=400, detail="Invitation has expired")

    # Check if invitation is still valid
    if not invitation.is_valid:
        raise HTTPException(status_code=400, detail="Invitation is no longer valid")

    return invitation


def process_invitation(db: Session, invite_code: str, user_id: int):
    # Get valid invitation
    invitation = get_invitation_by_code(db, invite_code)

    # Check if user exists
    user = db.query(User).filter(User.email == invitation.email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {invitation.email} not found")
    if user.id != user_id:
        raise HTTPException(status_code=401, detail=f"This Invite is for {invitation.email}")


    # Add user to organisation
    org_user = OrganisationUser(
        user_id=user.id,
        organisation_id=invitation.organisation_id,
        role="member"
    )
    db.add(org_user)

    # Add user to team if specified
    if invitation.team_id:
        team_user = TeamUser(
            user_id=user.id,
            team_id=invitation.team_id,
            role="member"
        )
        db.add(team_user)

    # Mark invitation as used
    invitation.is_valid = False

    db.commit()

    return {"status": "success", "message": f"User added to organisation {invitation.organisation_id} and team {invitation.team_id}"}
