import json
import math

def calculate_angle(a, b):
    return math.degrees(math.atan2(b['y'] - a['y'], b['x'] - a['x']))

def calculate_length(a, b):
    return math.sqrt((b['x'] - a['x'])**2 + (b['y'] - a['y'])**2)

def convert_to_spine(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    spine_data = {
        "skeleton": {"hash": " ", "spine": "4.2.35", "width": 1000, "height": 1000},
        "bones": [
            {"name": "root"},
            {"name": "hips", "parent": "root"},
            {"name": "leftHip", "parent": "hips"},
            {"name": "rightHip", "parent": "hips"},
            {"name": "spine", "parent": "hips"},
            {"name": "chest", "parent": "spine"},
            {"name": "neck", "parent": "chest"},
            {"name": "head", "parent": "neck"},
            {"name": "leftShoulder", "parent": "chest"},
            {"name": "leftUpperArm", "parent": "leftShoulder"},
            {"name": "leftElbow", "parent": "leftUpperArm"},
            {"name": "leftForearm", "parent": "leftElbow"},
            {"name": "leftHand", "parent": "leftForearm"},
            # {"name": "leftHandThumb", "parent": "leftHand"},
            # {"name": "leftHandIndex", "parent": "leftHand"},
            # {"name": "leftHandPinky", "parent": "leftHand"},
            {"name": "rightShoulder", "parent": "chest"},
            {"name": "rightUpperArm", "parent": "rightShoulder"},
            {"name": "rightElbow", "parent": "rightUpperArm"},
            {"name": "rightForearm", "parent": "rightElbow"},
            {"name": "rightHand", "parent": "rightForearm"},
            # {"name": "rightHandThumb", "parent": "rightHand"},
            # {"name": "rightHandIndex", "parent": "rightHand"},
            # {"name": "rightHandPinky", "parent": "rightHand"},
            {"name": "leftUpperLeg", "parent": "leftHip"},
            {"name": "leftKnee", "parent": "leftUpperLeg"},
            {"name": "leftLowerLeg", "parent": "leftKnee"},
            {"name": "leftFoot", "parent": "leftLowerLeg"},
            # {"name": "leftToe", "parent": "leftFoot"},
            {"name": "rightUpperLeg", "parent": "rightHip"},
            {"name": "rightKnee", "parent": "rightUpperLeg"},
            {"name": "rightLowerLeg", "parent": "rightKnee"},
            {"name": "rightFoot", "parent": "rightLowerLeg"},
            # {"name": "rightToe", "parent": "rightFoot"}
        ],
        "slots": [],
        "skins": {"default": {}},
        "animations": {"animation": {"bones": {}}}
    }

    fps = data["fps"]
    frames = data["frames"]
    scale_factor = 500

    for bone in spine_data["bones"]:
        spine_data["animations"]["animation"]["bones"][bone["name"]] = {"translate": [], "rotate": []}

    bone_connections = [
        ("hips", 23, 24),
        ("leftHip", 23, 23),
        ("rightHip", 24, 24),
        ("spine", 23, 11),
        ("chest", 11, 12),
        ("neck", 12, 0),
        ("head", 0, 0),
        ("leftShoulder", 11, 13),
        ("leftUpperArm", 13, 15),
        ("leftElbow", 15, 15),
        ("leftForearm", 15, 17),
        ("leftHand", 17, 19),
        # ("leftHandThumb", 19, 21),
        # ("leftHandIndex", 19, 20),
        # ("leftHandPinky", 19, 17),
        ("rightShoulder", 12, 14),
        ("rightUpperArm", 14, 16),
        ("rightElbow", 16, 16),
        ("rightForearm", 16, 18),
        ("rightHand", 18, 20),
        # ("rightHandThumb", 20, 22),
        # ("rightHandIndex", 20, 21),
        # ("rightHandPinky", 20, 18),
        ("leftUpperLeg", 23, 25),
        ("leftKnee", 25, 25),
        ("leftLowerLeg", 25, 27),
        ("leftFoot", 27, 31),
        # ("leftToe", 31, 29),
        ("rightUpperLeg", 24, 26),
        ("rightKnee", 26, 26),
        ("rightLowerLeg", 26, 28),
        ("rightFoot", 28, 32),
        # ("rightToe", 32, 30)
    ]

    for frame in frames:
        frame_num = frame["frame"]
        time = frame_num / fps
        landmarks = frame["landmarks"]

        def get_pos(index):
            return {
                "x": landmarks[index]["x"] * scale_factor,
                "y": landmarks[index]["y"] * scale_factor
            }

        root_position = get_pos(23)  # Use left hip as root

        for bone_name, start_idx, end_idx in bone_connections:
            start = get_pos(start_idx)
            end = get_pos(end_idx)
            
            angle = calculate_angle(start, end)
            length = calculate_length(start, end)
            
            spine_data["animations"]["animation"]["bones"][bone_name]["translate"].append({
                "time": time,
                "x": start["x"] - root_position["x"],
                "y": start["y"] - root_position["y"]
            })
            spine_data["animations"]["animation"]["bones"][bone_name]["rotate"].append({
                "time": time,
                "angle": angle
            })

        # Set root motion
        spine_data["animations"]["animation"]["bones"]["root"]["translate"].append({
            "time": time,
            "x": root_position["x"],
            "y": root_position["y"]
        })

    with open(output_file, 'w') as f:
        json.dump(spine_data, f, indent=2)

    print(f"Spine animation data saved to {output_file}")

# Usage
# convert_to_spine("landmarks_output.json", "spine_animation.json")