import cv2
import numpy as np
from ultralytics import YOLO, SAM
import argparse

def process_video(video_path, output_path):
    # Load models - Ultralytics will handle caching automatically
    yolo_model = YOLO("yolo11n.pt")
    sam2_model = SAM("sam2_b.pt")

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect people using YOLO model
        yolo_results = yolo_model(frame)

        # Filter for person class (adjust the class index if needed)
        person_boxes = yolo_results[0].boxes[yolo_results[0].boxes.cls == 0].xyxy.cpu().numpy()

        # Use SAM 2 for segmentation
        sam_results = sam2_model(frame, bboxes=person_boxes)

        # Combine all person masks
        combined_mask = np.zeros(frame.shape[:2], dtype=bool)
        for mask in sam_results[0].masks.data:
            combined_mask |= mask.cpu().numpy()

        # Apply the mask to the original frame
        segmented_frame = frame.copy()
        segmented_frame[~combined_mask] = [
            0,
            255,
            0,
        ]  # Green background, you can change this

        out.write(segmented_frame)

    cap.release()
    out.release()


def main():

    parser = argparse.ArgumentParser(description="Process video with YOLO and SAM2")
    parser.add_argument("input_video", help="Path to the input video file")
    parser.add_argument("output_video", help="Path to the output video file")
    args = parser.parse_args()

    process_video(args.input_video, args.output_video)

if __name__ == "__main__":
    main()
