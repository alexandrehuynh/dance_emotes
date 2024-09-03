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
    
    # Root
    root = bones.new("root")
    root.head = (0, 0, 0)
    root.tail = (0, 0, 0.1)
    
    # Spine
    spine = bones.new("spine")
    spine.head = (0, 0, 0.1)
    spine.tail = (0, 0, 0.5)
    spine.parent = root
    
    # Head
    head = bones.new("head")
    head.head = (0, 0, 0.5)
    head.tail = (0, 0, 0.7)
    head.parent = spine
    
    # Arms
    for side in ["left", "right"]:
        shoulder = bones.new(f"{{side}}_shoulder")
        shoulder.head = (0.2 if side == "right" else -0.2, 0, 0.5)
        shoulder.tail = (0.4 if side == "right" else -0.4, 0, 0.4)
        shoulder.parent = spine
        
        upper_arm = bones.new(f"{{side}}_upper_arm")
        upper_arm.head = shoulder.tail
        upper_arm.tail = (0.6 if side == "right" else -0.6, 0, 0.2)
        upper_arm.parent = shoulder
        
        forearm = bones.new(f"{{side}}_forearm")
        forearm.head = upper_arm.tail
        forearm.tail = (0.8 if side == "right" else -0.8, 0, 0)
        forearm.parent = upper_arm
        
        hand = bones.new(f"{{side}}_hand")
        hand.head = forearm.tail
        hand.tail = (0.9 if side == "right" else -0.9, 0, 0)
        hand.parent = forearm
    
    # Legs
    for side in ["left", "right"]:
        thigh = bones.new(f"{{side}}_thigh")
        thigh.head = (0.1 if side == "right" else -0.1, 0, 0)
        thigh.tail = (0.1 if side == "right" else -0.1, 0, -0.5)
        thigh.parent = root
        
        shin = bones.new(f"{{side}}_shin")
        shin.head = thigh.tail
        shin.tail = (0.1 if side == "right" else -0.1, 0, -0.9)
        shin.parent = thigh
        
        foot = bones.new(f"{{side}}_foot")
        foot.head = shin.tail
        foot.tail = (0.1 if side == "right" else -0.1, 0.2, -0.9)
        foot.parent = shin
    
    bpy.ops.object.mode_set(mode='OBJECT')
    return armature_object

def set_bone_keyframe(armature_object, bone_name, frame, location, rotation):
    if bone_name not in armature_object.pose.bones:
        print(f"Warning: Bone '{{bone_name}}' not found in the armature.")
        return

    pose_bone = armature_object.pose.bones[bone_name]
    
    pose_bone.location = location
    pose_bone.keyframe_insert(data_path="location", frame=frame)
    
    pose_bone.rotation_mode = 'QUATERNION'
    pose_bone.rotation_quaternion = rotation
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
        "root": 0,  # Nose (as a central point)
        "spine": 23,  # Left hip
        "head": 0,  # Nose
        "left_shoulder": 11,
        "left_upper_arm": 13,
        "left_forearm": 15,
        "left_hand": 19,
        "right_shoulder": 12,
        "right_upper_arm": 14,
        "right_forearm": 16,
        "right_hand": 20,
        "left_thigh": 23,
        "left_shin": 25,
        "left_foot": 27,
        "right_thigh": 24,
        "right_shin": 26,
        "right_foot": 28
    }}
    
    # Set keyframes for each frame
    for frame in data['frames']:
        frame_num = frame['frame']
        landmarks = frame['landmarks']
        
        for bone_name, landmark_idx in bone_mapping.items():
            landmark = landmarks[landmark_idx]
            location = (landmark['x'], landmark['y'], landmark['z'])
            
            # For simplicity, we'll use identity quaternion for rotation
            rotation = (1, 0, 0, 0)
            
            set_bone_keyframe(armature_object, bone_name, frame_num, location, rotation)
    
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