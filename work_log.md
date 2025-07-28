![img.png =1920*](img.png)

dissertation overleaf link: https://www.overleaf.com/project/686799ae3e3952171e3ca758

------------------------------------------
# week one, 1/7/2025 - 8/7/2025

1st meeting with professor 

project goal: the project will include an app that takes the hand gesture pictures as the input from a live stream. The app will convert the gesture into certain commands to control the smart device, just like using a keyboard and a cursor but touchless.

Upload every file into onedrive

supposed to do:
- [x]  research proposal
- [x]  methodology
- [x]  what kind of information i need from people
- [x] gesture design
- [ ] data collection

## 2/7/2025
- [x] research proposal
- [x] gesture design
- [x] start the writing on overleaf

gesture designed, should include distinguishable gestures, and use combination of gestures to cover every basic commands on OS.
writing on overleaf: https://www.overleaf.com/project/686799ae3e3952171e3ca758

## 3/7/2025
- [x] start the git repository, work log, documents
- [x] write the script of extracting frames from video
- [x] write the gesture design part into dissertation

git repo: https://github.com/AidanZhong/HandGestureRecog.git

## 4/7/2025
- [x] switch to correct template of dissertation using UoN's template
- [x] fill the correct ethic check form
- [x] fill the DMP(Data management plan)
- [ ] data collection

## 7/7/2025
- [x] data collected from 4 people

--------------------

# week two
- [ ] more literature review
- [ ] build the model
- [ ] methodology

write them down, which type is more demanded in industry in the future
1. explainable deep learning, maybe for medical imaging for example, the MRIs, CTs, could be interpretable
2. More VR/AR/MR based technology based on CV. For example stress monitoring, simulation training
3. Maybe combine some of the SLAM technology and experience i had before

## data preprocessing
- [ ] extract frames from the video and store it, label it
- [ ] extract features/skeleton from images and store it in a csv

# week three
- [ ] read 3 papers about hand gesture recognition
- [ ] trying to train my own model to extract the finger skeleton from images (AT LEAST try with 2 methods)

### 18/7/2025
![img_1.png](img_1.png)
read paper 'https://arxiv.org/abs/2406.03599'
core idea: Automatically generate 583k RGB images of hands using a consumer PC. It does not need any manual label.
Pipeline:
- Render diverse hand poses with high-quality 3D models.
- Train a CNN on this synthetic dataset
- Use domain adaption techniques to close the gap between generated data and real-world data.

It outperform those trained on real data, especially under occlusion.

### 19/7/2025
![img_2.png](img_2.png)
read paper 'https://arxiv.org/abs/2503.05995'
core idea: Introduce an efficient, lightweight network that predicts 2D keypoints, 3D keypoints, and full hand mesh from a single RGB image

### 20/7/2025
Combine the idea of the two article, I got my thought. Since it only need to classify only 8 gestures and they differs from each other.

My pipline is this:

--------------------
RGB Image

↓

Skeleton Estimator (CNN → Heatmaps)

↓

Extract 2D landmarks from heatmaps ← ignore occluded joints

↓

Classifier (MLP / CNN / LSTM) on 2D landmarks

↓

One of 8 Gesture Classes

----------------------

What I learnt from the papers
From Hi5:
- Focus on 2D landmark prediction only (no 3D, no mesh)
- Dont need labeled real data
- If occluded, just output visible keypoints - no need to hallucinate

From ReJSHand:
- Use a lightweighted heatmap regression network to predict 2D keypoints
- No mesh head, just the heatmap head for 21 joints

### 21/7/2025
Module 1: Skeleton predictor
Shallow CNN produces heatmaps
- input: RGB image
- Output: 21 heatmaps
- Loss: MSE between predicted heatmaps and ground truth gaussians
set occluded joints to None, to avoid unnecessary calculation

Module 2: Gesture Classifier
Take the 2D joint coordinates (21 * 2 vector), and classify into 8 gestures
Loss: Cross entropy

#### I need synthetic dataset generator
Use Blender Python API, which is widely used in Hi5-style pipelines
Randomized:
- hand pose (joint angles)
- Camera, viewpoint
- Light condition, background

Output:
RGB images, with list of 21 2D joint coordinates

## week 3
- [ ] prove 8 gestures are enough by my model, when my model is working proficiently
- [ ] finish the most part before 22nd August

todo:
- [ ] finish the 2D hand skeleton estimator
- [ ] train the classifier model

### 28/7/2025


## week 4