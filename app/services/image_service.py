from PIL import Image, ImageDraw, ImageFont
import os
from app.config import IMAGES_DIR, IMAGE_SIZE, TEXT_COLOR, BACKGROUND_COLOR, FONT_PATH, FONT_SIZE, TEXT_WRAP_WIDTH
from app.utils.file_manager import get_file_path

def create_image_with_text(text: str, image_index: int) -> str:
    """Creates an image with the given text and returns the file path."""
    img = Image.new('RGB', IMAGE_SIZE, color = BACKGROUND_COLOR)
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"Warning: Font file not found at {FONT_PATH}. Using default font.")
        font = ImageFont.load_default()

    # Wrap text
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if font.getlength(' '.join(current_line)) > IMAGE_SIZE[0] - 40: # 20px padding on each side
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    lines.append(' '.join(current_line))
    wrapped_text = "\n".join(lines)

    # Calculate text size and position to center it
    bbox = d.textbbox((0,0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (IMAGE_SIZE[0] - text_width) / 2
    y = (IMAGE_SIZE[1] - text_height) / 2

    d.text((x, y), wrapped_text, fill=TEXT_COLOR, font=font, align="center")

    image_filename = f"frame_{image_index}.png"
    image_filepath = get_file_path(IMAGES_DIR, image_filename)
    img.save(image_filepath)
    return image_filepath
