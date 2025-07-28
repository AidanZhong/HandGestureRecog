"""
Author: Aidan Zhong
Date: 2025/7/28 10:36
Description:
"""
import os

import smplx
import torch
import trimesh

mano_path = 'handpose'
model_path = os.path.join(mano_path, 'handPose_0.pkl')

model = smplx.create(
    model_path=mano_path,
    model_type='mano',
    flat_hand_mean=True,
    is_rhand=True,
    use_pca=False,
)

pose = torch.zeros([1, model.NUM_JOINTS * 3])
shape = torch.zeros([1, 10])

result = model(hand_pose=pose, betas=shape, return_verts=True, global_orient=torch.zeros([1, 3]))
vertices = result.vertices.detach().cpu().numpy().squeeze()
joints = result.joints.detach().cpu().numpy().squeeze()

mesh = trimesh.Trimesh(vertices,  model.faces, process=False)
mesh.export('test.obj')