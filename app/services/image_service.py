from PIL import Image, ImageDraw, ImageFont
import os
from app.config import IMAGES_DIR, IMAGE_SIZE, TEXT_COLOR, BACKGROUND_COLOR, FONT_PATH, FONT_SIZE, TEXT_WRAP_WIDTH
from app.utils.file_manager import get_file_path

def create_image_with_text(text: str, image_index: int) -> str:
    """Creates an image with the given text and returns the file path."""
    # Create a transparent image
    img = Image.new('RGBA', IMAGE_SIZE, (0, 0, 0, 0)) # Transparent background
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
        # Check if adding the next word exceeds the width
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

    # Draw a semi-transparent white background box behind the text
    padding = 20 # Padding around the text
    box_x1 = x - padding
    box_y1 = y - padding
    box_x2 = x + text_width + padding
    box_y2 = y + text_height + padding
    d.rectangle([(box_x1, box_y1), (box_x2, box_y2)], fill=(255, 255, 255, 180)) # White with 180 alpha

    # Draw the text in black
    d.text((x, y), wrapped_text, fill=(0, 0, 0), font=font, align="center")

    image_filename = f"frame_{image_index}.png"
    image_filepath = get_file_path(IMAGES_DIR, image_filename)
    img.save(image_filepath)
    return image_filepath