from elevenlabs.client import ElevenLabs
import os
from app.config import AUDIO_DIR, ELEVENLABS_API_KEY
from app.utils.file_manager import get_file_path

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

async def generate_audio_from_text(text: str, sentence_index: int) -> str:
    """Generates an audio file from text using ElevenLabs and returns the file path."""
    
    audio = client.text_to_speech.convert(
        voice_id="IuRRIAcbQK5AQk1XevPj", # You can change the voice as needed
        text=text,
        model_id="eleven_multilingual_v2"
    )

    audio_filename = f"sentence_{sentence_index}.mp3"
    audio_filepath = get_file_path(AUDIO_DIR, audio_filename)

    with open(audio_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)
        
    return audio_filepath
