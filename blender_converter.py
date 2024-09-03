import json
import os

def generate_blender_script(input_file, output_file):
    # Get absolute paths
    input_file_abs = os.path.abspath(input_file)
    output_file_abs = os.path.abspath(output_file)
    
    # Get the directory of the output file
    output_dir = os.path.dirname(output_file_abs)
    script_path = os.path.join(output_dir, "blender_conversion_script.py")

    script_content = f"""
import bpy
import json
from mathutils import Vector

def create_humanoid_armature():
    armature = bpy.data.armatures.new("MediaPipeArmature")
    armature_object = bpy.data.objects.new("MediaPipeArmature", armature)
    
    bpy.context.scene.collection.objects.link(armature_object)
    bpy.context.view_layer.objects.active = armature_object
    bpy.ops.object.mode_set(mode='EDIT')
    
    bones = armature.edit_bones
    
    # Create bones
    root = bones.new("root")
    spine = bones.new("spine")
    spine.parent = root
    neck = bones.new("neck")
    neck.parent = spine
    head = bones.new("head")
    head.parent = neck
    
    # Arms
    for side in ["left", "right"]:
        shoulder = bones.new(f"{{side}}_shoulder")
        shoulder.parent = spine
        upper_arm = bones.new(f"{{side}}_upper_arm")
        upper_arm.parent = shoulder
        forearm = bones.new(f"{{side}}_forearm")
        forearm.parent = upper_arm
        hand = bones.new(f"{{side}}_hand")
        hand.parent = forearm
    
    # Legs
    for side in ["left", "right"]:
        hip = bones.new(f"{{side}}_hip")
        hip.parent = root
        thigh = bones.new(f"{{side}}_thigh")
        thigh.parent = hip
        shin = bones.new(f"{{side}}_shin")
        shin.parent = thigh
        foot = bones.new(f"{{side}}_foot")
        foot.parent = shin
    
    bpy.ops.object.mode_set(mode='OBJECT')
    return armature_object

def set_bone_keyframe(armature_object, bone_name, frame, start, end):
    pose_bone = armature_object.pose.bones[bone_name]
    
    # Set location (only for root)
    if bone_name == "root":
        pose_bone.location = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, (start[2] + end[2]) / 2)
        pose_bone.keyframe_insert(data_path="location", frame=frame)
    
    # Set rotation
    direction = Vector((end[0] - start[0], end[1] - start[1], end[2] - start[2]))
    pose_bone.rotation_mode = 'QUATERNION'
    pose_bone.rotation_quaternion = direction.to_track_quat('Y', 'Z')
    pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)

def convert_mediapipe_to_blender(input_file, output_file):
    # Load MediaPipe data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Create armature
    armature_object = create_humanoid_armature()
    
    # Create animation data
    armature_object.animation_data_create()
    action = bpy.data.actions.new(name="MediaPipeAnimation")
    armature_object.animation_data.action = action
    
    # MediaPipe landmark to bone mapping
    bone_mapping = {{
        "root": (23, 24),  # Left hip, right hip
        "spine": (23, 11),  # Left hip, left shoulder
        "neck": (11, 12),  # Left shoulder, right shoulder
        "head": (0, 1),  # Nose, left eye inner
        "left_shoulder": (11, 13),
        "left_upper_arm": (13, 15),
        "left_forearm": (15, 17),
        "left_hand": (17, 19),
        "right_shoulder": (12, 14),
        "right_upper_arm": (14, 16),
        "right_forearm": (16, 18),
        "right_hand": (18, 20),
        "left_hip": (23, 25),
        "left_thigh": (25, 27),
        "left_shin": (27, 31),
        "left_foot": (29, 31),
        "right_hip": (24, 26),
        "right_thigh": (26, 28),
        "right_shin": (28, 32),
        "right_foot": (30, 32)
    }}
    
    # Set keyframes for each frame
    for frame in data['frames']:
        frame_num = frame['frame']
        landmarks = frame['landmarks']
        
        for bone_name, (start_idx, end_idx) in bone_mapping.items():
            start = landmarks[start_idx]
            end = landmarks[end_idx]
            set_bone_keyframe(armature_object, bone_name, frame_num, 
                              (start['x'], start['y'], start['z']),
                              (end['x'], end['y'], end['z']))
    
    # Save the Blender file
    bpy.ops.wm.save_as_mainfile(filepath=output_file)
    print(f"Animation imported from {{input_file}} and saved to {{output_file}}")


# Run the conversion
convert_mediapipe_to_blender("{input_file_abs}", "{output_file_abs}")
"""

    with open(script_path, "w") as f:
        f.write(script_content)

    print(f"Blender conversion script generated: {script_path}")
    print("To use this script:")
    print("1. Open Blender")
    print("2. Go to Scripting workspace")
    print("3. Open the generated script in the Text Editor")
    print("4. Click 'Run Script' or press Alt+P")

    return script_path

# Usage
# generate_blender_script("landmarks_output.json", "blender_animation.blend")