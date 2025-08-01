import math
import os
import random

import bpy
import bpy_extras.object_utils
import mathutils
import numpy as np
import trimesh
from mathutils import Vector

# === Paths ===
ply_dir = "/Users/qinkunzhong/PycharmProjects/HandGestureRecog/scripts/auto_generator/handsOnly_REGISTRATIONS_r_lm___POSES"
npy_dir = "/Users/qinkunzhong/PycharmProjects/HandGestureRecog/scripts/auto_generator/joint_coordinates"
output_dir = "/Users/qinkunzhong/PycharmProjects/HandGestureRecog/scripts/auto_generator/ply2obj2img"
os.makedirs(output_dir, exist_ok=True)


# === Utility ===
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


def generate_random_skin_colour():
    colors = [
        (0.87, 0.72, 0.53, 1.0),  # white
        (0.72, 0.54, 0.36, 1.0),  # yellow
        (0.51, 0.37, 0.26, 1.0)  # black
    ]
    base = random.choice(colors)
    variation = [random.uniform(-0.05, 0.05) for _ in range(3)] + [0.0]
    result = (min(max(b + v, 0.0), 1.0) for b, v in zip(base, variation))  # ensure the value is in 0~1
    return tuple(result)


def generate_random_background():
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes

    # Clear existing nodes to avoid mismatch
    for node in nodes:
        nodes.remove(node)

    # Create new background setup
    bg_node = nodes.new(type='ShaderNodeBackground')
    output_node = nodes.new(type='ShaderNodeOutputWorld')

    # Set random color (dark tones)
    bg_node.inputs[0].default_value = (
        random.uniform(0.0, 0.2),
        random.uniform(0.0, 0.2),
        random.uniform(0.0, 0.2),
        1.0
    )

    # Link nodes
    links = world.node_tree.links
    links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])


def generate_random_light():
    light = bpy.data.objects["Light"]
    light.location = (
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        random.uniform(1, 2)
    )
    light.data.energy = random.uniform(500, 1500)


def generate_random_transform():
    scale = random.uniform(1.5, 3.0)
    x_rotation = random.uniform(0, math.radians(360))
    y_rotation = random.uniform(0, math.radians(360))
    z_rotation = random.uniform(0, math.radians(360))
    return scale, x_rotation, y_rotation, z_rotation


def apply_random_transform(obj, scale, x_rotation, y_rotation, z_rotation):
    obj.scale = (scale, scale, scale)
    obj.rotation_euler = (x_rotation, y_rotation, z_rotation)


def build_transform_matrix(scale, x_rotation, y_rotation, z_rotation):
    scale_matrix = mathutils.Matrix().Scale(scale, 4)
    rot_matrix = mathutils.Euler((x_rotation, y_rotation, z_rotation), 'XYZ').to_matrix().to_4x4()
    return rot_matrix @ scale_matrix


setup_scene()
scene = bpy.context.scene
cam = scene.camera
width, height = scene.render.resolution_x, scene.render.resolution_y


def project_to_2d(world_point):
    """Project 3D point in world space to 2D image coords"""
    co_3d = Vector(world_point)
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, co_3d)
    u = int(co_2d.x * width)
    v = int((1 - co_2d.y) * height)  # flip y cooridnate
    return u, v


# === process ply files ===
for ply_file in sorted(os.listdir(ply_dir)):
    if not ply_file.endswith(".ply"):
        continue

    print(f"Rendering {ply_file}...")

    reset_scene()
    setup_scene()

    scene = bpy.context.scene
    cam = scene.camera
    width, height = scene.render.resolution_x, scene.render.resolution_y

    mesh = trimesh.load(os.path.join(ply_dir, ply_file), process=False)
    verts = np.array(mesh.vertices)
    faces = np.array(mesh.faces)

    # Create Blender mesh
    bl_mesh = bpy.data.meshes.new(name="HandMesh")
    bl_mesh.from_pydata(verts.tolist(), [], faces.tolist())
    bl_mesh.update()

    obj = bpy.data.objects.new("HandObject", bl_mesh)
    bpy.context.collection.objects.link(obj)

    # Add skin-tone material
    if "SkinMaterial" not in bpy.data.materials:
        mat = bpy.data.materials.new(name="SkinMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
    else:
        mat = bpy.data.materials["SkinMaterial"]
        bsdf = mat.node_tree.nodes["Principled BSDF"]

    bsdf.inputs["Base Color"].default_value = generate_random_skin_colour()
    obj.data.materials.append(mat)

    # transform
    scale, x_rotation, y_rotation, z_rotation = generate_random_transform()
    apply_random_transform(obj, scale, x_rotation, y_rotation, z_rotation)
    # random background
    generate_random_background()
    # random light
    generate_random_light()

    # === Load corresponding joint file ===
    base = os.path.splitext(ply_file)[0]
    joint_path = os.path.join(npy_dir, base + ".npy")
    if not os.path.exists(joint_path):
        print(f"⚠️ Joint file not found for {base}")
        continue

    joints_3d = np.load(joint_path)

    # === Project to 2D ===
    joints_2d = []
    transform_matrix = build_transform_matrix(scale, x_rotation, y_rotation, z_rotation)
    for joint in joints_3d:
        vec = Vector(joint).to_4d()
        transformed_vec = transform_matrix @ vec
        u, v = project_to_2d(transformed_vec.xyz)
        joints_2d.append((u, v))

    # === Save 2D joints to CSV ===
    joint_csv_path = os.path.join(output_dir, base + "_joints2d.csv")
    with open(joint_csv_path, "w") as f:
        f.write("u,v\n")
        for u, v in joints_2d:
            f.write(f"{u},{v}\n")

    # === Set render output path ===
    bpy.context.scene.render.filepath = os.path.join(output_dir, f"{base}.png")

    # === Render and cleanup ===
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(obj, do_unlink=True)
