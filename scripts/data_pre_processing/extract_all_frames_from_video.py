"""
Author: Aidan Zhong
Date: 2025/7/3 17:38
Description:
"""
import os

import cv2


def extract_frames(video_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    frame_count = 0
    skip_frames = 0

    # Loop through video frames
    while video.isOpened():
        success, frame = video.read()
        if not success:
            skip_frames += 1
            print(f'{skip_frames} frames read failed, skipped')
            frame_count += 1
            if frame_count >= total_frames:
                break
            continue

        frame_filename = os.path.join(output_dir, f"frame_{frame_count:05d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

        if frame_count % 100 == 0:
            print(f"Extracted {frame_count}/{total_frames} frames...")

    video.release()
    print(f"Finished extracting frames. Total frames saved: {frame_count}")


def handle_videos(root_folder):
    result_folder = os.path.join(root_folder, "result")
    for filename in os.listdir(root_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(root_folder, filename)
            output_dir = os.path.join(result_folder, filename.rstrip(".mp4"))
            extract_frames(video_path, output_dir)


v_path = ['../../data/dataset2']
for v in v_path:
    handle_videos(v)
