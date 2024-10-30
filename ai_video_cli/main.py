import argparse
from ai_video_cli.commands import (
    split_video,
    combine_videos,
    replace_audio,
    generate_thumbnail,
    convert_video,
    extract_audio
)

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
        help="Replace the audio of a video with an audio file",
    )
    replace_audio_parser.add_argument("input_video", help="Input video file")
    replace_audio_parser.add_argument(
        "input_audio", help="Audio file to use as replacement"
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

    # Convert command
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert a video to specific video and audio codecs, with optional cropping",
    )
    convert_parser.add_argument("input_file", help="Input video file")
    convert_parser.add_argument(
        "output_file",
        nargs="?",
        help="Output video file (optional, default: <input_file>_converted.<ext>)",
    )
    convert_parser.add_argument(
        "--video_codec",
        default="libx264",
        help="Video codec to use (default: libx264)",
    )
    convert_parser.add_argument(
        "--audio_codec",
        default="aac",
        help="Audio codec to use (default: aac)",
    )
    convert_parser.add_argument(
        "--crop_width",
        type=int,
        default=1280,
        help="Width to crop the video (default: 1280)",
    )
    convert_parser.add_argument(
        "--crop_height",
        type=int,
        default=768,
        help="Height to crop the video (default: 768)",
    )

    # Extract audio command
    extract_audio_parser = subparsers.add_parser(
        "extract_audio", help="Extract audio from a video file"
    )
    extract_audio_parser.add_argument("input_file", help="Input video file")
    extract_audio_parser.add_argument(
        "output_file",
        nargs="?",
        help="Output audio file (optional, default: <input_file>_audio.mp3)",
    )

    args = parser.parse_args()

    if args.command == "split":
        split_video(args.input_file, args.chunk_size)
    elif args.command == "combine":
        combine_videos(args.output_file, args.input_files, args.codec)
    elif args.command == "replace_audio":
        replace_audio(args.input_video, args.input_audio, args.output_file)
    elif args.command == "thumbnail":
        generate_thumbnail(args.input_file, args.output_file)
    elif args.command == "convert":
        convert_video(
            args.input_file,
            args.output_file,
            args.video_codec,
            args.audio_codec,
            args.crop_width,
            args.crop_height,
        )
    elif args.command == "extract_audio":
        extract_audio(args.input_file, args.output_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
