from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
import os

from oauth import (
    oauth,
    register_oauth_providers,
    get_or_create_user_from_oauth,
    get_google_user_info,
    get_github_user_info,
    create_access_token,
    OAuthUserInfo,
)

app = FastAPI()

register_oauth_providers()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/slopengine"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = UserDB(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.email != db_user.email:
        existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

    db_user.email = user.email
    db_user.password_hash = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.get("/auth/google")
async def google_auth(request: Request):
    redirect_uri = request.url_for("google_auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/google/callback")
async def google_auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await get_google_user_info(token)
    user = await get_or_create_user_from_oauth(db, user_info)

    access_token = create_access_token(data={"sub": user.email, "provider": "google"})

    return {"access_token": access_token, "token_type": "bearer", "user": user_info}


@app.get("/auth/github")
async def github_auth(request: Request):
    redirect_uri = request.url_for("github_auth_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@app.get("/auth/github/callback")
async def github_auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    user_info = await get_github_user_info(token)
    user = await get_or_create_user_from_oauth(db, user_info)

    access_token = create_access_token(data={"sub": user.email, "provider": "github"})

    return {"access_token": access_token, "token_type": "bearer", "user": user_info}


@app.get("/auth/providers")
async def get_oauth_providers():
    providers = []
    if "google" in oauth._clients:
        providers.append(
            {"name": "google", "url": "/auth/google", "display_name": "Google"}
        )
    if "github" in oauth._clients:
        providers.append(
            {"name": "github", "url": "/auth/github", "display_name": "GitHub"}
        )
    return {"providers": providers}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
