import json
import os

def generate_blender_script(input_file, output_file):
    # Get the directory of the output file
    output_dir = os.path.dirname(output_file)
    script_path = os.path.join(output_dir, "blender_conversion_script.py")

    script_content = f"""
import bpy
import json
import math

def create_armature():
    # Create armature and object
    armature = bpy.data.armatures.new("DanceArmature")
    armature_object = bpy.data.objects.new("DanceArmature", armature)
    
    # Link armature object to the scene
    bpy.context.scene.collection.objects.link(armature_object)
    
    # Make armature active and go to edit mode
    bpy.context.view_layer.objects.active = armature_object
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Create bones
    bones = armature.edit_bones
    
    # Add bones (adjust as needed based on your MediaPipe data)
    bones.new("hips")
    bones.new("spine").parent = bones["hips"]
    bones.new("chest").parent = bones["spine"]
    bones.new("neck").parent = bones["chest"]
    bones.new("head").parent = bones["neck"]
    
    # Add arm bones
    for side in ["left", "right"]:
        shoulder = bones.new(f"{{side}}_shoulder")
        shoulder.parent = bones["chest"]
        upper_arm = bones.new(f"{{side}}_upper_arm")
        upper_arm.parent = shoulder
        forearm = bones.new(f"{{side}}_forearm")
        forearm.parent = upper_arm
        hand = bones.new(f"{{side}}_hand")
        hand.parent = forearm
    
    # Add leg bones
    for side in ["left", "right"]:
        thigh = bones.new(f"{{side}}_thigh")
        thigh.parent = bones["hips"]
        shin = bones.new(f"{{side}}_shin")
        shin.parent = thigh
        foot = bones.new(f"{{side}}_foot")
        foot.parent = shin
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return armature_object

def set_bone_keyframe(action, bone_name, frame, start_landmark, end_landmark):
    # Calculate bone position and rotation
    x = (start_landmark["x"] + end_landmark["x"]) / 2
    y = (start_landmark["y"] + end_landmark["y"]) / 2
    z = (start_landmark["z"] + end_landmark["z"]) / 2
    
    # Calculate rotation (you might need to adjust this based on your coordinate system)
    rotation = calculate_bone_rotation(start_landmark, end_landmark)
    
    # Set keyframe
    for i, value in enumerate([x, y, z]):
        fcurve = action.fcurves.new(data_path=f'pose.bones["{{bone_name}}"].location', index=i)
        keyframe = fcurve.keyframe_points.insert(frame, value)
    
    for i, value in enumerate(rotation):
        fcurve = action.fcurves.new(data_path=f'pose.bones["{{bone_name}}"].rotation_euler', index=i)
        keyframe = fcurve.keyframe_points.insert(frame, value)

def calculate_bone_rotation(start, end):
    # Calculate rotation based on bone direction
    # This is a simplified calculation and might need adjustment
    dx = end["x"] - start["x"]
    dy = end["y"] - start["y"]
    dz = end["z"] - start["z"]
    
    # Convert to Euler angles (XYZ order)
    rotX = math.atan2(dy, dz)
    rotY = math.atan2(-dx, math.sqrt(dy*dy + dz*dz))
    rotZ = 0  # You might need to calculate this based on your needs
    
    return (rotX, rotY, rotZ)

def convert_mediapipe_to_blender(input_file):
    # Load MediaPipe data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Create armature
    armature_object = create_armature()
    
    # Create animation data
    armature_object.animation_data_create()
    action = bpy.data.actions.new(name="DanceAnimation")
    armature_object.animation_data.action = action
    
    # Set up key frames
    fps = data["fps"]
    frames = data["frames"]
    
    for frame in frames:
        frame_num = frame["frame"]
        landmarks = frame["landmarks"]
        
        # Set keyframes for each bone
        # (You'll need to adjust this based on your specific bone setup and MediaPipe data)
        set_bone_keyframe(action, "hips", frame_num, landmarks[23], landmarks[24])
        set_bone_keyframe(action, "spine", frame_num, landmarks[23], landmarks[11])
        set_bone_keyframe(action, "chest", frame_num, landmarks[11], landmarks[12])
        set_bone_keyframe(action, "neck", frame_num, landmarks[12], landmarks[0])
        
        # Set keyframes for arms and legs...
    
    print(f"Animation imported from {{input_file}}")

# Run the conversion
convert_mediapipe_to_blender("{input_file}")

# Save the Blender file
bpy.ops.wm.save_as_mainfile(filepath="{output_file}")
print(f"Blender file saved as {{output_file}}")
"""

    with open(script_path, "w") as f:
        f.write(script_content)

    print(f"Blender conversion script generated: {script_path}")
    print("To use this script:")
    print("1. Open Blender")
    print("2. Go to Scripting workspace")
    print("3. Open the generated script in the Text Editor")
    print("4. Click 'Run Script' or press Alt+P")

# Usage
# generate_blender_script("landmarks_output.json", "blender_animation.blend")