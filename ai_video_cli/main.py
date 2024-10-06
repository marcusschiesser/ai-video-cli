import argparse
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
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

        while start_time < video_duration:
            end_time = min(start_time + chunk_size, video_duration)
            part_filename = f"{base_filename}_part{part_num}{ext}"
            video.subclip(start_time, end_time).write_videofile(
                part_filename, codec=codec
            )
            print(f"Saved chunk: {part_filename}")
            start_time = end_time
            part_num += 1
    except Exception as e:
        print(f"Error: {e}")


def combine_videos(output_file, input_files, codec=None):
    try:
        video_clips = [VideoFileClip(file) for file in input_files]
        combined = concatenate_videoclips(video_clips)
        codec = codec if codec else get_video_codec(video_clips[0])
        combined.write_videofile(output_file, codec=codec)
        print(f"Combined video saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")


def replace_audio(input_video, audio_video, output_file=None):
    try:
        if output_file is None:
            base_filename, ext = os.path.splitext(input_video)
            output_file = f"{base_filename}_with_replaced_audio{ext}"

        video = VideoFileClip(input_video)
        audio_clip = VideoFileClip(audio_video)

        # Get audio from the audio video and adjust duration to match video duration
        audio = audio_clip.audio
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        else:
            audio = audio.fx(vfx.loop, duration=video.duration)

        # write video with new audio
        video_with_new_audio = video.set_audio(audio)
        video_with_new_audio.write_videofile(
            output_file,
            codec=get_video_codec(video),
            audio_codec=get_audio_codec(audio_clip),
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


def main():
    parser = argparse.ArgumentParser(description="AI Video Editor CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Split command
    split_parser = subparsers.add_parser(
        "split", help="Split a video into chunks of 5 or 10 seconds"
    )
    split_parser.add_argument("input_file", help="Input video file")
    split_parser.add_argument(
        "--chunk_size",
        type=int,
        choices=[5, 10],
        default=10,
        help="Chunk size in seconds (default: 10)",
    )

    # Combine command
    combine_parser = subparsers.add_parser(
        "combine", help="Combine multiple videos into one"
    )
    combine_parser.add_argument("output_file", help="Output video file")
    combine_parser.add_argument(
        "--codec", help="Optional codec to use for the output video, e.g. 'libx264'"
    )
    combine_parser.add_argument(
        "input_files", nargs="+", help="Input video files to combine"
    )

    # Replace audio command
    replace_audio_parser = subparsers.add_parser(
        "replace_audio",
        help="Replace the audio of a video with the audio from another video",
    )
    replace_audio_parser.add_argument("input_video", help="Input video file")
    replace_audio_parser.add_argument(
        "audio_video", help="Video file to take audio from"
    )
    replace_audio_parser.add_argument(
        "output_file",
        nargs="?",
        help="Output video file with replaced audio (optional)",
    )

    # Thumbnail command
    thumbnail_parser = subparsers.add_parser(
        "thumbnail", help="Generate a thumbnail from the first frame of a video"
    )
    thumbnail_parser.add_argument("input_file", help="Input video file")
    thumbnail_parser.add_argument(
        "output_file",
        nargs="?",
        help="Output thumbnail file (optional, default: <input_file>_thumbnail.jpg)",
    )

    args = parser.parse_args()

    if args.command == "split":
        split_video(args.input_file, args.chunk_size)
    elif args.command == "combine":
        combine_videos(args.output_file, args.input_files, args.codec)
    elif args.command == "replace_audio":
        replace_audio(args.input_video, args.audio_video, args.output_file)
    elif args.command == "thumbnail":
        generate_thumbnail(args.input_file, args.output_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
