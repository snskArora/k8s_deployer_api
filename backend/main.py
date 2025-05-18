from .database import engine, Base
from .routers import invite, user

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Organization and Team Management API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(invite.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Organization and Team Management API"}


@app.get("/invite/{invite_code}")
async def process_invite(invite_code: str):
    """
    This is a special route to handle invitations.

    When a user visits this URL, the frontend should:
    1. Check if the user is authenticated
    2. If not, redirect to login/signup
    3. After authentication, accept the invitation for the authenticated user

    This endpoint simply returns the invite code for the frontend to handle.
    """
    return {"invite_code": invite_code, "message": "Use this code with the /invitations/accept/{invite_code} endpoint"}
