from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Video generation schemas
class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: int = 10
    resolution: str = "1920x1080"
    style: Optional[str] = None
    fps: int = 30


class VideoGenerationResponse(BaseModel):
    video_id: str
    status: str
    message: str
    created_at: datetime


# OAuth schemas
class OAuthUserInfo(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    provider: str
