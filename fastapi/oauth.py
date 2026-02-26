from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.config import Config

from main import get_db, UserDB

config = Config(".env")

oauth = OAuth(config)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class OAuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class OAuthUserInfo(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    provider: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    provider: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        provider: str = payload.get("provider", "local")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, provider=provider)
    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(UserDB.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserDB = Depends(get_current_user)):
    return current_user


def register_oauth_providers():
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    github_client_id = os.getenv("GITHUB_CLIENT_ID")
    github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

    if google_client_id and google_client_secret:
        oauth.register(
            name="google",
            client_id=google_client_id,
            client_secret=google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )

    if github_client_id and github_client_secret:
        oauth.register(
            name="github",
            client_id=github_client_id,
            client_secret=github_client_secret,
            access_token_url="https://github.com/login/oauth/access_token",
            authorize_url="https://github.com/login/oauth/authorize",
            api_base_url="https://api.github.com/",
            client_kwargs={"scope": "user:email"},
        )


async def get_or_create_user_from_oauth(
    db: Session, user_info: OAuthUserInfo
) -> UserDB:
    user = db.query(UserDB).filter(UserDB.email == user_info.email).first()

    if not user:
        user = UserDB(
            email=user_info.email,
            password_hash=f"oauth_{user_info.provider}_{user_info.id}",
            created_at=datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


async def get_google_user_info(token: dict) -> OAuthUserInfo:
    userinfo = await oauth.google.userinfo(token=token)
    return OAuthUserInfo(
        id=userinfo.get("sub"),
        email=userinfo.get("email"),
        name=userinfo.get("name"),
        picture=userinfo.get("picture"),
        provider="google",
    )


async def get_github_user_info(token: dict) -> OAuthUserInfo:
    async with oauth.github.get("user", token=token) as resp:
        user_data = await resp.json()

    async with oauth.github.get("user/emails", token=token) as resp:
        emails = await resp.json()

    primary_email = next(
        (email["email"] for email in emails if email.get("primary")), None
    )

    return OAuthUserInfo(
        id=str(user_data.get("id")),
        email=primary_email or user_data.get("email"),
        name=user_data.get("name"),
        picture=user_data.get("avatar_url"),
        provider="github",
    )
