"""
Author: Aidan Zhong
Date: 2025/7/14 19:07
Description:
"""
import csv
import os

import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils


def extract_pose_features_from_video(video_file, show):
    print(f'processing {video_file}')
    cap = cv2.VideoCapture(video_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    frame_count = 0
    skip_frames = 0

    output_csv = video_file.replace('.mp4', '.csv')
    header = [
        "frame", "landmark_index", "x", "y", "z", "visibility"
    ]

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                skip_frames += 1
                print(f'{skip_frames} frames read failed, skipped')
                frame_count += 1
                if frame_count >= total_frames:
                    break
                continue
            frame_count += 1

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(rgb_frame)

            if results.pose_landmarks and show:
                mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )

            if results.pose_landmarks:
                for index, landmark in enumerate(results.pose_landmarks.landmark):
                    csv_writer.writerow([
                        frame_count,
                        index,
                        landmark.x,
                        landmark.y,
                        landmark.z,
                        landmark.visibility
                    ])

            if results.pose_world_landmarks and show:
                mp_drawing.draw_landmarks(
                    frame, results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS
                )

            if show:
                cv2.imshow(video_file, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return output_csv


def extract_from_a_folder(root_folder):
    for filename in os.listdir(root_folder):
        if filename.endswith(".mp4"):
            extract_pose_features_from_video(os.path.join(root_folder, filename), True)


if __name__ == '__main__':
    file = '../../data/dataset1/result/g1_00'
    v_path = [file]
    for v in v_path:
        extract_from_a_folder(v)
