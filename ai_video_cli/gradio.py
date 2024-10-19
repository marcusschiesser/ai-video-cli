import gradio as gr
from ai_video_cli.main import split_video

def split_video_interface(input_file, chunk_size):
    try:
        split_files = split_video(input_file.name, chunk_size)
        if not split_files:
            return None, "No files were created."
        
        return split_files, "Video split successfully."
    except Exception as e:
        return None, f"Error: {str(e)}"

iface = gr.Interface(
    fn=split_video_interface,
    inputs=[
        gr.File(label="Input Video File"),
        gr.Radio([5, 10], label="Chunk Size (seconds)", value=10)
    ],
    outputs=[
        gr.Files(label="Split Video Files"),
        gr.Textbox(label="Result")
    ],
    title="Video Splitter",
    description="Split a video into chunks of 5 or 10 seconds."
)

def launch():
    iface.launch()

if __name__ == "__main__":
    launch()
