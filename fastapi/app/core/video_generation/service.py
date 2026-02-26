import os
import uuid
from typing import Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpy
import tempfile

from app.config import settings
from app.models.schemas import VideoGenerationRequest, VideoGenerationResponse


class VideoGenerationService:
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for video generation")

        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=self.openai_api_key,
        )

        # Prompt template for enhancing video prompts
        self.prompt_enhancer = PromptTemplate(
            input_variables=["prompt", "style"],
            template="""You are a video generation expert. Enhance the following video prompt for better results.

Original prompt: {prompt}
Style: {style}

Enhanced prompt (be specific, descriptive, and cinematic):""",
        )

        self.enhancer_chain = LLMChain(llm=self.llm, prompt=self.prompt_enhancer)

    def generate_video(
        self, request: VideoGenerationRequest
    ) -> VideoGenerationResponse:
        video_id = str(uuid.uuid4())

        # Enhance the prompt using LLM
        enhanced_prompt = self.enhancer_chain.run(
            prompt=request.prompt,
            style=request.style or "cinematic",
        )

        # Parse resolution
        width, height = map(int, request.resolution.split("x"))

        # Create a simulated video (in production, this would call Sora API)
        video_path = self._create_simulated_video(
            video_id=video_id,
            prompt=enhanced_prompt,
            duration=request.duration,
            width=width,
            height=height,
            fps=request.fps,
        )

        return VideoGenerationResponse(
            video_id=video_id,
            status="completed",
            message=f"Video generated successfully: {enhanced_prompt}",
            created_at=datetime.utcnow(),
        )

    def _create_simulated_video(
        self,
        video_id: str,
        prompt: str,
        duration: int,
        width: int,
        height: int,
        fps: int,
    ) -> str:
        # Create a temporary directory for video files
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, f"{video_id}.mp4")

        # Create frames
        frames = []
        for i in range(duration * fps):
            # Create a simple animated frame based on prompt
            frame = self._create_frame(
                prompt=prompt,
                frame_num=i,
                total_frames=duration * fps,
                width=width,
                height=height,
            )
            frames.append(frame)

        # Create video from frames
        clip = mpy.ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(video_path, codec="libx264", audio=False)

        # In production, save to persistent storage (S3, etc.)
        # For now, we'll just return the path
        return video_path

    def _create_frame(
        self,
        prompt: str,
        frame_num: int,
        total_frames: int,
        width: int,
        height: int,
    ) -> np.ndarray:
        # Create a simple gradient background
        img = Image.new("RGB", (width, height), color="black")
        draw = ImageDraw.Draw(img)

        # Add some text with the prompt
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # Draw animated elements
        progress = frame_num / total_frames

        # Gradient effect
        for y in range(height):
            color_value = int(255 * (y / height) * progress)
            draw.line([(0, y), (width, y)], fill=(color_value, color_value, 255))

        # Draw prompt text
        text = f"Video: {prompt[:50]}..."
        text_width = draw.textlength(text, font=font)
        text_position = ((width - text_width) // 2, height // 2)
        draw.text(text_position, text, fill="white", font=font)

        # Progress indicator
        bar_width = int(width * 0.8)
        bar_height = 20
        bar_x = (width - bar_width) // 2
        bar_y = height // 2 + 50
        draw.rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], outline="white"
        )
        draw.rectangle(
            [bar_x, bar_y, bar_x + int(bar_width * progress), bar_y + bar_height],
            fill="white",
        )

        return np.array(img)

    def get_video_path(self, video_id: str) -> Optional[str]:
        # In production, retrieve from storage
        # For simulation, check if file exists
        temp_dir = tempfile.gettempdir()
        video_path = os.path.join(temp_dir, f"{video_id}.mp4")

        if os.path.exists(video_path):
            return video_path
        return None
