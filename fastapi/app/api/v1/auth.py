from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.dependencies import get_db
from app.models.schemas import UserCreate, UserResponse, Token, LoginRequest
from app.services.user_service import UserService
from app.core.oauth.base import (
    oauth,
    register_oauth_providers,
    get_google_user_info,
    get_github_user_info,
    get_or_create_user_from_oauth,
    create_oauth_access_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])

# Register OAuth providers
register_oauth_providers()


@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.create_user(user_create)
    return user


@router.post("/login", response_model=Token)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.authenticate(login_request.email, login_request.password)
    access_token = user_service.create_auth_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/oauth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/oauth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await get_google_user_info(token)
        user = get_or_create_user_from_oauth(db, user_info)
        access_token = create_oauth_access_token(user)

        # Redirect to frontend with token
        frontend_url = (
            f"{request.app.state.frontend_url}/oauth/callback?token={access_token}"
        )
        return RedirectResponse(url=frontend_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth failed: {str(e)}",
        )


@router.get("/oauth/github")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/oauth/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.github.authorize_access_token(request)
        user_info = await get_github_user_info(token)
        user = get_or_create_user_from_oauth(db, user_info)
        access_token = create_oauth_access_token(user)

        # Redirect to frontend with token
        frontend_url = (
            f"{request.app.state.frontend_url}/oauth/callback?token={access_token}"
        )
        return RedirectResponse(url=frontend_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub OAuth failed: {str(e)}",
        )
