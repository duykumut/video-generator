from moviepy.editor import AudioFileClip, ImageSequenceClip, CompositeVideoClip, VideoFileClip, ImageClip, CompositeAudioClip, concatenate_audioclips
import os
from app.config import VIDEOS_DIR, FPS, IMAGE_SIZE, TEMPLATE_DIR
from app.utils.file_manager import get_file_path

async def create_video_from_audio_and_images(audio_filepaths: list[str], image_filepaths: list[str], output_filename: str, template_name: str = None) -> str:
    """Combines audio files and image files into a single video, optionally using a template video."""
    final_video_filepath = get_file_path(VIDEOS_DIR, output_filename)

    audio_clips = [AudioFileClip(ap) for ap in audio_filepaths]
    total_duration = sum(c.duration for c in audio_clips)

    if template_name:
        template_filepath = os.path.join(TEMPLATE_DIR, template_name)
        template_video = VideoFileClip(template_filepath).resize(IMAGE_SIZE)
        template_video = template_video.set_duration(total_duration)

        final_clips = [template_video]
        current_time = 0

        for i, audio_clip in enumerate(audio_clips):
            image_clip = ImageClip(image_filepaths[i]).set_duration(audio_clip.duration).set_start(current_time).set_pos(("center", "center"))
            final_clips.append(image_clip)
            current_time += audio_clip.duration

        final_clip = CompositeVideoClip(final_clips, size=IMAGE_SIZE)
        final_clip = final_clip.set_audio(concatenate_audioclips(audio_clips))

    else:
        clips = []
        current_time = 0

        for i, audio_path in enumerate(audio_filepaths):
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            image_clip = ImageSequenceClip([image_filepaths[i]], fps=FPS)
            image_clip = image_clip.set_duration(duration)
            image_clip = image_clip.set_audio(audio_clip)
            image_clip = image_clip.set_start(current_time)

            clips.append(image_clip)
            current_time += duration

        final_clip = CompositeVideoClip(clips, size=IMAGE_SIZE)

    final_clip.write_videofile(final_video_filepath, fps=FPS, codec="libx264", audio_codec="aac")

    return final_video_filepath
