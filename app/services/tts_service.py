from gtts import gTTS
import os
from app.config import AUDIO_DIR
from app.utils.file_manager import get_file_path

async def generate_audio_from_text(text: str, sentence_index: int) -> str:
    """Generates an audio file from text using gTTS and returns the file path."""
    tts = gTTS(text=text, lang='tr') # You can change language as needed
    audio_filename = f"sentence_{sentence_index}.mp3"
    audio_filepath = get_file_path(AUDIO_DIR, audio_filename)
    tts.save(audio_filepath)
    return audio_filepath
