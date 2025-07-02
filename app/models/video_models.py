from pydantic import BaseModel
from typing import Optional, List

class VideoGenerationRequest(BaseModel):
    text: str

class VideoGenerationResponse(BaseModel):
    video_url: str

class GenerateAndUploadRequest(BaseModel):
    text: str
    music_name: Optional[str] = None
    template_name: Optional[str] = None
    youtube_title: str
    youtube_description: Optional[str] = None
    youtube_tags: Optional[List[str]] = None
    youtube_privacy_status: str = "private"