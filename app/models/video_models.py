from pydantic import BaseModel

class VideoGenerationRequest(BaseModel):
    text: str

class VideoGenerationResponse(BaseModel):
    video_url: str
