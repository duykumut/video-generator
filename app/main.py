from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import uuid

from app.config import VIDEOS_DIR, STATIC_DIR
from app.models.video_models import VideoGenerationRequest, VideoGenerationResponse
from app.services.text_processor import split_text_into_sentences
from app.services.tts_service import generate_audio_from_text
from app.services.image_service import create_image_with_text
from app.services.video_service import create_video_from_audio_and_images
from app.utils.file_manager import clean_temp_dirs

app = FastAPI()

# Statik dosyaları bağlama
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template dizinini belirtme
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_short", response_class=HTMLResponse)
async def generate_short(request: Request, text: str = Form(...)):
    clean_temp_dirs()

    sentences = split_text_into_sentences(text)

    audio_filepaths = []
    image_filepaths = []

    for i, sentence in enumerate(sentences):
        audio_path = await generate_audio_from_text(sentence, i)
        audio_filepaths.append(audio_path)

        image_path = create_image_with_text(sentence, i)
        image_filepaths.append(image_path)

    output_filename = f"short_{uuid.uuid4()}.mp4"
    final_video_filepath = await create_video_from_audio_and_images(audio_filepaths, image_filepaths, output_filename)

    # Convert absolute path to relative URL for frontend
    relative_video_path = os.path.relpath(final_video_filepath, STATIC_DIR)
    generated_video_url = f"/static/{relative_video_path}"

    return templates.TemplateResponse("result.html", {"request": request, "video_url": generated_video_url})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)