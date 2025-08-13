"""
Author: Aidan Zhong
Date: 2025/1/14 14:19
Description:
"""
import cv2
import numpy as np
# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
from matplotlib import pyplot as plt

# Load the input image.
image_path = '../../data/dataset2/result/g1_00/frame_00000.jpg'
image = tf.io.read_file(image_path)
image = tf.compat.v1.image.decode_jpeg(image)
image = tf.expand_dims(image, axis=0)
# Resize and pad the image to keep the aspect ratio and fit the expected size.
image = tf.cast(tf.image.resize_with_pad(image, 256, 256), dtype=tf.int32)

# Download the model from TF Hub.
model = hub.load("https://www.kaggle.com/models/google/movenet/TensorFlow2/multipose-lightning/1")
movenet = model.signatures['serving_default']

# Run model inference.
outputs = movenet(image)
# Output is a [1, 6, 56] tensor.
keypoints = outputs['output_0'].numpy()  # [1, 6, 56] tensor (batch, max_people, keypoints)

# Extract the keypoints for the first detected person
person_keypoints = keypoints[0, 0, :]  # Select first person (if any)
keypoints_reshaped = person_keypoints[:51].reshape(-1, 3)  # Reshape to [17, 3]: x, y, confidence

# Convert normalized keypoints to original image coordinates
original_height, original_width, _ = image.shape
keypoints_scaled = np.array([
    (kp[1] * original_height, kp[0] * original_width, kp[2])  # y, x, confidence
    for kp in keypoints_reshaped
])

# Visualize the keypoints on the original image
def draw_keypoints(image, keypoints, threshold=0.3):
    """Draw keypoints on the image."""
    for kp in keypoints:
        y, x, confidence = kp
        if confidence > threshold:  # Only draw keypoints above confidence threshold
            cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)

# Draw the keypoints
image_with_keypoints = cv2.cvtColor(image.numpy(), cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
draw_keypoints(image_with_keypoints, keypoints_scaled)

# Display the image with keypoints using matplotlib
plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(image_with_keypoints, cv2.COLOR_BGR2RGB))  # Convert back to RGB for visualization
plt.axis('off')
plt.show()