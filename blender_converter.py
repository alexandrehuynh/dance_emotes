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
import math
from mathutils import Vector, Quaternion

def create_humanoid_armature(initial_landmarks):
    armature = bpy.data.armatures.new("MediaPipeArmature")
    armature_object = bpy.data.objects.new("MediaPipeArmature", armature)
    
    bpy.context.scene.collection.objects.link(armature_object)
    bpy.context.view_layer.objects.active = armature_object
    bpy.ops.object.mode_set(mode='EDIT')
    
    bones = armature.edit_bones
    
    hip_landmark = initial_landmarks[23]  # Left hip as reference
    
    # Adjusted bone structure
    bone_structure = {{
        "spine": (23, 11),  # Left hip to left shoulder
        "neck": (11, 0),  # Left shoulder to nose
        "left_shoulder": (11, 13),
        "left_upper_arm": (13, 15),
        "left_forearm": (15, 17),
        "left_hand": (17, 19),
        "right_shoulder": (12, 14),
        "right_upper_arm": (14, 16),
        "right_forearm": (16, 18),
        "right_hand": (18, 20),
        "left_thigh": (23, 25),
        "left_shin": (25, 27),
        "left_foot": (27, 31),
        "right_thigh": (24, 26),
        "right_shin": (26, 28),
        "right_foot": (28, 32)
    }}
    
    for bone_name, (start_idx, end_idx) in bone_structure.items():
        bone = bones.new(bone_name)
        start_pos = convert_coordinates(initial_landmarks[start_idx], hip_landmark)
        end_pos = convert_coordinates(initial_landmarks[end_idx], hip_landmark)
        
        bone.head = start_pos
        bone.tail = end_pos
        
        if bone_name.startswith("left_") or bone_name.startswith("right_"):
            parent_name = "_".join(bone_name.split("_")[:-1])
            bone.parent = bones.get(parent_name)
        elif bone_name == "neck":
            bone.parent = bones.get("spine")
    
    # Ensure the armature is standing upright
    bpy.ops.object.mode_set(mode='OBJECT')
    armature_object.rotation_euler = (math.radians(90), 0, 0)
    
    return armature_object
    
def convert_coordinates(landmark, hip_landmark):
    x = (landmark['x'] - hip_landmark['x'])
    y = -(landmark['z'] - hip_landmark['z'])  # Negate for depth
    z = -(landmark['y'] - hip_landmark['y'])  # Negate to invert Y axis
    return (x, y, z)

def calculate_bone_rotation(start_pos, end_pos):
    # Calculate bone direction
    direction = (Vector(end_pos) - Vector(start_pos)).normalized()
    
    # Create a rotation quaternion that aligns the bone with this direction
    up_vector = Vector((0, 0, 1))
    rotation = direction.to_track_quat('Y', 'Z')
    
    return rotation

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
    
    if not data['frames']:
        print("Error: No frame data found in the input file.")
        return
    
    # Create armature based on the first frame of data
    initial_landmarks = data['frames'][0]['landmarks']
    armature_object = create_humanoid_armature(initial_landmarks)
    
    # Create animation data
    armature_object.animation_data_create()
    action = bpy.data.actions.new(name="MediaPipeAnimation")
    armature_object.animation_data.action = action
    
    # MediaPipe landmark to bone mapping
    bone_mapping = {{
        "root": (0, 23),
        "spine": (23, 24),
        "neck": (11, 12),
        "head": (0, 0),
        "left_shoulder": (11, 13),
        "left_upper_arm": (13, 15),
        "left_forearm": (15, 17),
        "left_hand": (17, 19),
        "right_shoulder": (12, 14),
        "right_upper_arm": (14, 16),
        "right_forearm": (16, 18),
        "right_hand": (18, 20),
        "left_thigh": (23, 25),
        "left_shin": (25, 27),
        "left_foot": (27, 31),
        "right_thigh": (24, 26),
        "right_shin": (26, 28),
        "right_foot": (28, 32)
    }}
    
    # Set keyframes for each frame
    for frame in data['frames']:
        frame_num = frame['frame']
        landmarks = frame['landmarks']
        hip_landmark = landmarks[23]  # Left hip as reference
        
        for bone_name, (start_idx, end_idx) in bone_mapping.items():
            try:
                start_landmark = landmarks[start_idx]
                end_landmark = landmarks[end_idx]
                
                start_pos = convert_coordinates(start_landmark, hip_landmark)
                end_pos = convert_coordinates(end_landmark, hip_landmark)
                
                # Use start position as location for the bone
                location = start_pos
                
                # Calculate rotation based on bone direction
                rotation = calculate_bone_rotation(start_pos, end_pos)
                
                set_bone_keyframe(armature_object, bone_name, frame_num, location, rotation)
            except IndexError:
                print(f"Warning: Missing landmark data for bone '{{bone_name}}' in frame {{frame_num}}")
    
    # Save the Blender file
    bpy.ops.wm.save_as_mainfile(filepath=output_file)
    print(f"Animation imported from {{input_file}} and saved to {{output_file}}")

# Global scale factor to adjust MediaPipe data to Blender's scale
SCALE_FACTOR = 8  # Adjust this value as needed

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