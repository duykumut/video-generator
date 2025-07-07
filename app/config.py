import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMP_DIR = os.path.join(STATIC_DIR, "temp")
AUDIO_DIR = os.path.join(TEMP_DIR, "audio")
IMAGES_DIR = os.path.join(TEMP_DIR, "images")
VIDEOS_DIR = os.path.join(TEMP_DIR, "videos")
TEMPLATE_DIR = os.path.join(STATIC_DIR, "templates")
MUSIC_DIR = os.path.join(STATIC_DIR, "music")

# Ensure template and music directories exist
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# Audio settings
MUSIC_VOLUME = 0.2 # 20% of original volume

# Ensure directories exist
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# Video settings
FPS = 24
IMAGE_SIZE = (1080, 1920) # YouTube Shorts resolution (portrait)
TEXT_COLOR = (0, 0, 0) # Black
BACKGROUND_COLOR = (255, 255, 255) # White
FONT_PATH = os.path.join(STATIC_DIR, "fonts", "Montserrat.ttf")
FONT_SIZE = 80
TEXT_WRAP_WIDTH = 20 # Characters per line before wrapping

# YouTube API Settings
# Place your client_secrets.json file in the root directory of the project.
# This file contains your OAuth 2.0 client ID and client secret.

# ElevenLabs API Key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")