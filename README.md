# AI Video Editor CLI Tool

A CLI tool for simple video editing tasks: splitting videos, combining videos, replacing audio, and generating thumbnails. Very useful for working with video-to-video AI models like [Runway](https://runwayml.com/)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- ffmpeg (for video processing), e.g. on MacOS use `brew install ffmpeg`

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/marcusschiesser/ai-video-cli.git
   cd ai-video-cli
   ```

2. Install dependencies using Poetry:
   ```
   poetry install 
   ```

3. Open shell:
   ```
   poetry shell
   ```

4. Run the tool:
   ```
   cd <directory_with_videos>
   ai-video [command] [arguments]
   ```

## Commands

The AI Video Editor CLI tool supports the following commands:

### 1. Split Video

Splits a video into chunks.

```
ai-video split <input_file> [--chunk_size {5,10}]
```

- `<input_file>`: Path to the input video file
- `--chunk_size`: Chunk size in seconds (default: 10)

Example:
```
ai-video split my_long_video.mp4 --chunk_size 5
```

This command will split `my_long_video.mp4` into 5-second chunks. The output files will be named 
`my_long_video_part1.mp4`, `my_long_video_part2.mp4`, and so on.


### 2. Combine Videos

Combines multiple videos into one.

```
ai-video combine <output_file> <input_files>... [--codec CODEC]
```

- `<output_file>`: Path to the output video file
- `<input_files>`: One or more input video files to combine
- `--codec`: Optional codec to use for the output video (e.g., 'libx264')

Example:
```
ai-video combine final_video.mp4 part1.mp4 part2.mp4 part3.mp4
```

This command will combine `part1.mp4`, `part2.mp4`, and `part3.mp4` into a single video file named `final_video.mp4`. The videos will be concatenated in the order they are specified.

### 3. Replace Audio

Replaces the audio of a video with the audio from another video.

```
ai-video replace_audio <input_video> <audio_video> [output_file]
```

- `<input_video>`: Path to the input video file whose audio will be replaced
- `<audio_video>`: Path to the video file from which the audio will be extracted
- `[output_file]`: Optional path for the output video file with replaced audio

Example:
```
ai-video replace_audio original_video.mp4 audio_source.mp4 final_video.mp4
```

This command will take the video from `original_video.mp4`, replace its audio with the audio from `audio_source.mp4`, and save the result as `final_video.mp4`.

If you don't specify an output file, the tool will automatically generate one.

### 4. Generate Thumbnail

Generates a thumbnail image from the first frame of a video.

```
ai-video thumbnail <input_file> [--output_file <output_file>]
```

- `<input_file>`: Path to the input video file
- `--output_file`: Optional path for the output thumbnail file (default: <input_file>_thumbnail.jpg)

Example:
```
ai-video thumbnail my_video.mp4
```

This command will generate a thumbnail from the first frame of `my_video.mp4` and save it as `my_video_thumbnail.jpg`.
