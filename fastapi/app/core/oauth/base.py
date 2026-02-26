from typing import Optional, Dict, Any
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.models.schemas import OAuthUserInfo
from app.core.security import get_password_hash, create_access_token


config = Config(".env")
oauth = OAuth(config)


def register_oauth_providers():
    if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
        oauth.register(
            name="google",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )

    if settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
        oauth.register(
            name="github",
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            access_token_url="https://github.com/login/oauth/access_token",
            authorize_url="https://github.com/login/oauth/authorize",
            api_base_url="https://api.github.com/",
            client_kwargs={"scope": "user:email"},
        )


async def get_google_user_info(token: Dict[str, Any]) -> OAuthUserInfo:
    user_info = await oauth.google.userinfo(token=token)
    return OAuthUserInfo(
        email=user_info.get("email"),
        name=user_info.get("name"),
        picture=user_info.get("picture"),
        provider="google",
    )


async def get_github_user_info(token: Dict[str, Any]) -> OAuthUserInfo:
    async with oauth.github.get("user", token=token) as resp:
        user_info = await resp.json()

    # Get email from GitHub
    async with oauth.github.get("user/emails", token=token) as resp:
        emails = await resp.json()
        primary_email = next(
            (
                email["email"]
                for email in emails
                if email.get("primary") and email.get("verified")
            ),
            None,
        )

    return OAuthUserInfo(
        email=primary_email or user_info.get("email"),
        name=user_info.get("name"),
        picture=user_info.get("avatar_url"),
        provider="github",
    )


def get_or_create_user_from_oauth(db: Session, oauth_user: OAuthUserInfo) -> User:
    user = db.query(User).filter(User.email == oauth_user.email).first()

    if not user:
        # Create new user with random password for OAuth users
        user = User(
            email=oauth_user.email,
            password_hash=get_password_hash("oauth_user_temp_password"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def create_oauth_access_token(user: User) -> str:
    return create_access_token(data={"sub": user.email})
