from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import uuid

from app.config import VIDEOS_DIR, STATIC_DIR, TEMPLATE_DIR, MUSIC_DIR
from app.models.video_models import VideoGenerationRequest, VideoGenerationResponse, GenerateAndUploadRequest
from app.services.text_processor import split_text_into_sentences
from app.services.tts_service import generate_audio_from_text
from app.services.image_service import create_image_with_text
from app.services.video_service import create_video_from_audio_and_images
from app.utils.file_manager import clean_temp_dirs
from app.services.youtube_service import upload_video_to_youtube

app = FastAPI()

# Statik dosyaları bağlama
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template dizinini belirtme
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    template_files = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith((".mp4", ".mov", ".avi"))]
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith((".mp3", ".wav"))]
    return templates.TemplateResponse("index.html", {"request": request, "templates": template_files, "musics": music_files})

@app.post("/generate_short", response_class=HTMLResponse)
async def generate_short(request: Request, text: str = Form(...), template_name: str = Form(""), music_name: str = Form("")):
    

    sentences = split_text_into_sentences(text)

    audio_filepaths = []
    image_filepaths = []

    for i, sentence in enumerate(sentences):
        audio_path = await generate_audio_from_text(sentence, i)
        audio_filepaths.append(audio_path)

        image_path = create_image_with_text(sentence, i)
        image_filepaths.append(image_path)

    output_filename = f"short_{uuid.uuid4()}.mp4"
    final_video_filepath = await create_video_from_audio_and_images(audio_filepaths, image_filepaths, output_filename, template_name, music_name)

    # Convert absolute path to relative URL for frontend
    relative_video_path = os.path.relpath(final_video_filepath, STATIC_DIR)
    generated_video_url = f"/static/{relative_video_path}"

    return templates.TemplateResponse("result.html", {"request": request, "video_url": generated_video_url, "video_filepath": final_video_filepath})

@app.post("/upload_to_youtube", response_class=HTMLResponse)
async def upload_to_youtube(request: Request,
                            video_filepath: str = Form(...),
                            title: str = Form(...),
                            description: str = Form(""),
                            tags: str = Form(""),
                            privacy_status: str = Form("private")):
    
    tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    youtube_video_url = await upload_video_to_youtube(video_filepath, title, description, tags_list, privacy_status)
    
    if youtube_video_url:
        return templates.TemplateResponse("youtube_upload_success.html", {"request": request, "youtube_video_url": youtube_video_url})
    else:
        return templates.TemplateResponse("youtube_upload_failure.html", {"request": request})

@app.post("/api/generate_and_upload_video", response_class=JSONResponse)
async def api_generate_and_upload_video(request_data: GenerateAndUploadRequest):
    try:
        sentences = split_text_into_sentences(request_data.text)

        audio_filepaths = []
        image_filepaths = []

        for i, sentence in enumerate(sentences):
            audio_path = await generate_audio_from_text(sentence, i)
            audio_filepaths.append(audio_path)

            image_path = create_image_with_text(sentence, i)
            image_filepaths.append(image_path)

        output_filename = f"short_{uuid.uuid4()}.mp4"
        final_video_filepath = await create_video_from_audio_and_images(
            audio_filepaths, 
            image_filepaths, 
            output_filename, 
            request_data.template_name, 
            request_data.music_name
        )

        youtube_video_url = await upload_video_to_youtube(
            final_video_filepath,
            request_data.youtube_title,
            request_data.youtube_description,
            request_data.youtube_tags,
            request_data.youtube_privacy_status
        )

        if youtube_video_url:
            return JSONResponse({"status": "success", "youtube_video_url": youtube_video_url})
        else:
            raise HTTPException(status_code=500, detail="Failed to upload video to YouTube.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)