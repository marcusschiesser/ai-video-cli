import math
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip
from PIL import Image

def get_video_codec(video):
    codec = getattr(video, "codec", None)
    if codec:
        print(f"Input video codec: {codec}")
    else:
        print("Codec information not available. Using default 'libx264'.")
        codec = "libx264"
    return codec

def get_audio_codec(audio_clip):
    audio_codec = getattr(audio_clip, "audio_codec", None)
    if not audio_codec:
        print("Audio codec information not available. Using default 'aac'.")
        audio_codec = "aac"
    else:
        print(f"Using audio codec: {audio_codec}")
    return audio_codec

def split_video(input_file, chunk_size):
    try:
        video = VideoFileClip(input_file)
        codec = get_video_codec(video)
        video_duration = video.duration
        base_filename, ext = os.path.splitext(input_file)

        start_time = 0
        part_num = 1
        split_files = []

        while start_time < video_duration:
            end_time = min(start_time + chunk_size, video_duration)
            part_filename = f"{base_filename}_part{part_num}{ext}"
            video.subclip(start_time, end_time).write_videofile(
                part_filename, codec=codec
            )
            print(f"Saved chunk: {part_filename}")
            split_files.append(part_filename)
            start_time = end_time
            part_num += 1

        return split_files
    except Exception as e:
        print(f"Error: {e}")
        return []

def combine_videos(output_file, input_files, codec=None):
    try:
        video_clips = [VideoFileClip(file) for file in input_files]
        combined = concatenate_videoclips(video_clips)
        codec = codec if codec else get_video_codec(video_clips[0])
        combined.write_videofile(output_file, codec=codec)
        print(f"Combined video saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def replace_audio(input_video, input_audio, output_file=None):
    try:
        if output_file is None:
            base_filename, ext = os.path.splitext(input_video)
            output_file = f"{base_filename}_with_replaced_audio{ext}"

        video = VideoFileClip(input_video)
        audio = AudioFileClip(input_audio)

        # Adjust audio duration to match video duration
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        else:
            audio = audio.fx(vfx.loop, duration=video.duration)

        # write video with new audio
        video_with_new_audio = video.set_audio(audio)
        video_with_new_audio.write_videofile(
            output_file,
            codec=get_video_codec(video),
            audio_codec=get_audio_codec(audio),
        )

        print(f"Audio replaced. Output video saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def generate_thumbnail(input_file, output_file=None):
    try:
        if output_file is None:
            base_filename, _ = os.path.splitext(input_file)
            output_file = f"{base_filename}_thumbnail.jpg"

        video = VideoFileClip(input_file)
        thumbnail = video.get_frame(0)  # Get the first frame
        video.close()

        # Save the thumbnail
        Image.fromarray(thumbnail).save(output_file)

        print(f"Thumbnail generated and saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def convert_video(
    input_file, output_file, video_codec, audio_codec, crop_width, crop_height
):
    try:
        video = VideoFileClip(input_file)

        # If output_file is not provided, create a default name
        if output_file is None:
            base_filename, ext = os.path.splitext(input_file)
            output_file = f"{base_filename}_converted{ext}"

        # Resize and crop the video if dimensions are provided
        if crop_width and crop_height:
            # Calculate the aspect ratios
            target_aspect = crop_width / crop_height
            video_aspect = video.w / video.h

            if video_aspect > target_aspect:
                # Video is wider, scale based on height
                new_height = crop_height
                new_width = int(math.ceil(new_height * video_aspect))
            else:
                # Video is taller, scale based on width
                new_width = crop_width
                new_height = int(math.ceil(new_width / video_aspect))

            # Resize the video
            resized_video = video.resize(height=new_height, width=new_width)

            # Calculate padding
            pad_x = max(0, (crop_width - new_width) // 2)
            pad_y = max(0, (crop_height - new_height) // 2)

            # Crop to final size
            final_video = resized_video.crop(
                x1=pad_x, y1=pad_y, width=crop_width, height=crop_height
            )
        else:
            final_video = video

        # Write the video file with specified codecs
        final_video.write_videofile(
            output_file, codec=video_codec, audio_codec=audio_codec
        )

        print(f"Video converted and saved as: {output_file}")
        print(f"Video codec: {video_codec}")
        print(f"Audio codec: {audio_codec}")
        if crop_width and crop_height:
            print(f"Video resized and cropped to: {crop_width}x{crop_height}")
    except Exception as e:
        print(f"Error: {e}")

def extract_audio(input_file, output_file=None):
    try:
        if output_file is None:
            base_filename, _ = os.path.splitext(input_file)
            output_file = f"{base_filename}_audio.mp3"

        video = VideoFileClip(input_file)
        audio = video.audio

        # Extract audio
        audio.write_audiofile(output_file)

        video.close()
        audio.close()

        print(f"Audio extracted and saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
