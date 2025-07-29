"""
Author: Aidan Zhong
Date: 2025/7/29 01:36
Description:
"""
import os

image_dir = "./"
label_dir = "./"

deleted = 0

for filename in os.listdir(image_dir):
    if not filename.endswith(".png"):
        continue

    base_name = filename.replace(".png", "")
    csv_name = f"{base_name}_joints2d.csv"
    csv_path = os.path.join(label_dir, csv_name)

    if not os.path.exists(csv_path):
        # CSV does not exist — delete the image
        img_path = os.path.join(image_dir, filename)
        os.remove(img_path)
        print(f"Deleted: {filename}")
        deleted += 1

print(f"Done. {deleted} .png files deleted.")