from moviepy.editor import AudioFileClip, ImageSequenceClip, CompositeVideoClip
import os
from app.config import VIDEOS_DIR, FPS, IMAGE_SIZE
from app.utils.file_manager import get_file_path

async def create_video_from_audio_and_images(audio_filepaths: list[str], image_filepaths: list[str], output_filename: str) -> str:
    """Combines audio files and image files into a single video."""
    final_video_filepath = get_file_path(VIDEOS_DIR, output_filename)

    clips = []
    current_time = 0

    for i, audio_path in enumerate(audio_filepaths):
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Use the corresponding image for the duration of the audio clip
        image_clip = ImageSequenceClip([image_filepaths[i]], fps=FPS)
        image_clip = image_clip.set_duration(duration)
        image_clip = image_clip.set_audio(audio_clip)
        image_clip = image_clip.set_start(current_time)

        clips.append(image_clip)
        current_time += duration

    final_clip = CompositeVideoClip(clips, size=IMAGE_SIZE)
    final_clip.write_videofile(final_video_filepath, fps=FPS, codec="libx264", audio_codec="aac")

    return final_video_filepath
