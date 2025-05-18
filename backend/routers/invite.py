from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..schemas.invite import InvitationCreate, Invitation
from ..services.auth import get_current_user
from ..services.invite import create_invitation, get_invitation_by_code, process_invitation

router = APIRouter(
    prefix="/invitations",
    tags=["invitations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Invitation)
def create_new_invitation(
    invitation: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new invitation to an organisation and optionally a team"""
    return create_invitation(
        db=db,
        organisation_id=invitation.organisation_id,
        email=invitation.email,
        team_id=invitation.team_id,
        expires_at=invitation.expires_at,
        created_by=current_user.id
    )


@router.get("/{invite_code}", response_model=Invitation)
def read_invitation(invite_code: str, db: Session = Depends(get_db)):
    """Get invitation details by invite code"""
    return get_invitation_by_code(db=db, invite_code=invite_code)


@router.post("/accept/{invite_code}")
def accept_invitation(
    invite_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept an invitation and add user to organisation/team"""
    return process_invitation(db=db, invite_code=invite_code, user_id=current_user.id)
