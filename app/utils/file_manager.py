import os
import shutil
from app.config import AUDIO_DIR, IMAGES_DIR, VIDEOS_DIR

def clean_temp_dirs():
    """Cleans up temporary audio, image, and video directories."""
    for directory in [AUDIO_DIR, IMAGES_DIR, VIDEOS_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)

def get_file_path(directory, filename):
    """Returns a full file path within a specified temporary directory."""
    return os.path.join(directory, filename)
