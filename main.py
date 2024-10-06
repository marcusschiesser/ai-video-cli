import argparse
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip


def split_video(input_file, chunk_size):
    try:
        video = VideoFileClip(input_file)
        video_duration = video.duration
        base_filename, ext = os.path.splitext(input_file)

        start_time = 0
        part_num = 1

        while start_time < video_duration:
            end_time = min(start_time + chunk_size, video_duration)
            part_filename = f"{base_filename}_part{part_num}{ext}"
            video.subclip(start_time, end_time).write_videofile(
                part_filename, codec=video.reader.codec
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
        codec = codec if codec else video_clips[0].reader.codec
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
        audio = VideoFileClip(audio_video).audio
        video = video.set_audio(audio)
        video.write_videofile(output_file, codec=video.reader.codec)
        print(f"Audio replaced. Output video saved as: {output_file}")
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

    args = parser.parse_args()

    if args.command == "split":
        split_video(args.input_file, args.chunk_size)
    elif args.command == "combine":
        combine_videos(args.output_file, args.input_files, args.codec)
    elif args.command == "replace_audio":
        replace_audio(args.input_video, args.audio_video, args.output_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
