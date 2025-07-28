"""
Author: Aidan Zhong
Date: 2025/7/28 18:38
Description:
"""

import bpy
import os
import math

input_dir = "/Users/qinkunzhong/PycharmProjects/HandGestureRecog/scripts/auto_generator/ply2obj"
output_dir = "/Users/qinkunzhong/PycharmProjects/HandGestureRecog/scripts/auto_generator/ply2obj2img"
os.makedirs(output_dir, exist_ok=True)

def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def setup_scene():
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(0.0, -1.5, 0.0), rotation=(math.radians(90), 0, 0))
    cam = bpy.data.objects["Camera"]
    cam.location = (0.0, -1.5, 0.0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam

    if "Light" not in bpy.data.objects:
        light_data = bpy.data.lights.new(name="Light", type='POINT')
        light_obj = bpy.data.objects.new(name="Light", object_data=light_data)
        bpy.context.collection.objects.link(light_obj)
        light_obj.location = (0.5, -0.5, 1.5)

    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512

setup_scene()

for obj_file in sorted(os.listdir(input_dir)):
    if not obj_file.endswith(".obj"):
        continue

    reset_scene()
    setup_scene()

    bpy.ops.import_scene.obj(filepath=os.path.join(input_dir, obj_file))

    base = os.path.splitext(obj_file)[0]
    bpy.context.scene.render.filepath = os.path.join(output_dir, f"{base}.png")
    bpy.ops.render.render(write_still=True)