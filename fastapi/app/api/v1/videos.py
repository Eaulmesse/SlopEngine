from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.schemas import VideoGenerationRequest, VideoGenerationResponse
from app.models.user import User
from app.models.video import GeneratedVideo
from app.core.security import get_current_active_user
from app.core.video_generation.service import VideoGenerationService


router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        # Initialize video service
        video_service = VideoGenerationService()

        # Generate video
        response = video_service.generate_video(request)

        # Save to database
        video_record = GeneratedVideo(
            video_id=response.video_id,
            user_id=current_user.id,
            prompt=request.prompt,
            duration=request.duration,
            resolution=request.resolution,
            style=request.style,
            fps=request.fps,
            video_path=f"generated_videos/{response.video_id}.mp4",
            status=response.status,
        )

        db.add(video_record)
        db.commit()

        return response

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video generation failed: {str(e)}",
        )


@router.get("/{video_id}")
async def get_video(
    video_id: str,
    current_user: User = Depends(get_current_active_user),
):
    # Check if user has access to this video
    video_service = VideoGenerationService()
    video_path = video_service.get_video_path(video_id)

    if not video_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        )

    # In production, check database for ownership
    # For now, return the file
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4",
    )


@router.get("/user/{user_id}")
async def get_user_videos(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Only allow users to view their own videos
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these videos",
        )

    videos = db.query(GeneratedVideo).filter(GeneratedVideo.user_id == user_id).all()
    return videos
