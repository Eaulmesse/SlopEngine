from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.models.base import Base


class GeneratedVideo(Base):
    __tablename__ = "generated_videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    prompt = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    resolution = Column(String, nullable=False)
    style = Column(String, nullable=True)
    fps = Column(Integer, nullable=False)
    video_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
