import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMP_DIR = os.path.join(STATIC_DIR, "temp")
AUDIO_DIR = os.path.join(TEMP_DIR, "audio")
IMAGES_DIR = os.path.join(TEMP_DIR, "images")
VIDEOS_DIR = os.path.join(TEMP_DIR, "videos")
TEMPLATE_DIR = os.path.join(STATIC_DIR, "templates")

# Ensure template directory exists
os.makedirs(TEMPLATE_DIR, exist_ok=True)

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
