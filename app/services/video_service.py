from moviepy.editor import AudioFileClip, ImageSequenceClip, CompositeVideoClip, VideoFileClip, ImageClip, CompositeAudioClip, concatenate_audioclips
import os
from app.config import VIDEOS_DIR, FPS, IMAGE_SIZE, TEMPLATE_DIR, MUSIC_DIR, MUSIC_VOLUME
from app.utils.file_manager import get_file_path

async def create_video_from_audio_and_images(audio_filepaths: list[str], image_filepaths: list[str], output_filename: str, template_name: str = None, music_name: str = None) -> str:
    """Combines audio files and image files into a single video, optionally using a template video and background music."""
    final_video_filepath = get_file_path(VIDEOS_DIR, output_filename)

    audio_clips = [AudioFileClip(ap) for ap in audio_filepaths]
    total_duration = sum(c.duration for c in audio_clips)

    final_audio_clip = concatenate_audioclips(audio_clips)

    if music_name:
        music_filepath = os.path.join(MUSIC_DIR, music_name)
        background_music = AudioFileClip(music_filepath)
        
        # Loop music if it's shorter than the video
        if background_music.duration < total_duration:
            background_music = background_music.loop(duration=total_duration)
        else:
            background_music = background_music.set_duration(total_duration)

        background_music = background_music.volumex(MUSIC_VOLUME)
        final_audio_clip = CompositeAudioClip([final_audio_clip, background_music])

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
        final_clip = final_clip.set_audio(final_audio_clip)

    else:
        clips = []
        current_time = 0

        for i, audio_clip in enumerate(audio_clips):
            image_clip = ImageSequenceClip([image_filepaths[i]], fps=FPS)
            image_clip = image_clip.set_duration(audio_clip.duration)
            image_clip = image_clip.set_audio(audio_clip)
            image_clip = image_clip.set_start(current_time)

            clips.append(image_clip)
            current_time += audio_clip.duration

        final_clip = CompositeVideoClip(clips, size=IMAGE_SIZE)
        final_clip = final_clip.set_audio(final_audio_clip)

    final_clip.write_videofile(final_video_filepath, fps=FPS, codec="libx264", audio_codec="aac")

    return final_video_filepath
