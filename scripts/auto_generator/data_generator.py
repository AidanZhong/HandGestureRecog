"""
Author: Aidan Zhong
Date: 2025/7/21 23:36
Description:
"""

import cv2
import numpy as np
import os
from pathlib import Path

def generate_synthetic_hand_image(image_size=256, num_joints=21):
    img = np.ones((image_size, image_size, 3), dtype=np.uint8) * 255  # white background
    joints = []

    center_x, center_y = image_size // 2, image_size // 2
    for i in range(num_joints):
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(10, 100)
        x = int(center_x + np.cos(angle) * radius)
        y = int(center_y + np.sin(angle) * radius)
        # make sure it does not goes out of the image
        x = np.clip(x, 0, image_size - 1)
        y = np.clip(y, 0, image_size - 1)
        joints.append((x, y))
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

    return img, np.array(joints, dtype=np.float32)

def generate_dataset(output_dir='synthetic_data', num_samples=500):
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/joints", exist_ok=True)

    for i in range(num_samples):
        img, joints = generate_synthetic_hand_image()
        img_path = f"{output_dir}/images/{i:04d}.png"
        joints_path = f"{output_dir}/joints/{i:04d}.npy"
        cv2.imwrite(img_path, img)
        np.save(joints_path, joints)

    print(f"Generated {num_samples} samples.")


if __name__ == "__main__":
    generate_dataset()