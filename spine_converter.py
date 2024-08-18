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
            {"name": "rightShoulder", "parent": "chest"},
            {"name": "rightUpperArm", "parent": "rightShoulder"},
            {"name": "rightElbow", "parent": "rightUpperArm"},
            {"name": "rightForearm", "parent": "rightElbow"},
            {"name": "rightHand", "parent": "rightForearm"},
            {"name": "leftUpperLeg", "parent": "leftHip"},
            {"name": "leftKnee", "parent": "leftUpperLeg"},
            {"name": "leftLowerLeg", "parent": "leftKnee"},
            {"name": "leftFoot", "parent": "leftLowerLeg"},
            {"name": "rightUpperLeg", "parent": "rightHip"},
            {"name": "rightKnee", "parent": "rightUpperLeg"},
            {"name": "rightLowerLeg", "parent": "rightKnee"},
            {"name": "rightFoot", "parent": "rightLowerLeg"},
        ],
        "slots": [
            {"name": "hips", "bone": "hips", "attachment": "line"},
            {"name": "spine", "bone": "spine", "attachment": "line"},
            {"name": "chest", "bone": "chest", "attachment": "line"},
            {"name": "neck", "bone": "neck", "attachment": "line"},
            {"name": "head", "bone": "head", "attachment": "line"},
            {"name": "leftUpperArm", "bone": "leftUpperArm", "attachment": "line"},
            {"name": "leftForearm", "bone": "leftForearm", "attachment": "line"},
            {"name": "leftHand", "bone": "leftHand", "attachment": "line"},
            {"name": "rightUpperArm", "bone": "rightUpperArm", "attachment": "line"},
            {"name": "rightForearm", "bone": "rightForearm", "attachment": "line"},
            {"name": "rightHand", "bone": "rightHand", "attachment": "line"},
            {"name": "leftUpperLeg", "bone": "leftUpperLeg", "attachment": "line"},
            {"name": "leftLowerLeg", "bone": "leftLowerLeg", "attachment": "line"},
            {"name": "leftFoot", "bone": "leftFoot", "attachment": "line"},
            {"name": "rightUpperLeg", "bone": "rightUpperLeg", "attachment": "line"},
            {"name": "rightLowerLeg", "bone": "rightLowerLeg", "attachment": "line"},
            {"name": "rightFoot", "bone": "rightFoot", "attachment": "line"},
        ],
        "skins": {
            "default": {
                "hips": {"hips": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
                "spine": {"spine": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
                "chest": {"chest": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
                "neck": {"neck": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 30, "height": 5}},
                "head": {"head": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 80, "height": 5}},
                "leftUpperArm": {"leftUpperArm": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 40, "height": 5}},
                "leftForearm": {"leftForearm": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 30, "height": 5}},
                "leftHand": {"leftHand": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 30, "height": 5}},
                "rightUpperArm": {"rightUpperArm": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 40, "height": 5}},
                "rightForearm": {"rightForearm": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 30, "height": 5}},
                "rightHand": {"rightHand": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 30, "height": 5}},
                "leftUpperLeg": {"leftUpperLeg": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 60, "height": 5}},
                "leftLowerLeg": {"leftLowerLeg": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
                "leftFoot": {"leftFoot": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
                "rightUpperLeg": {"rightUpperLeg": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 60, "height": 5}},
                "rightLowerLeg": {"rightLowerLeg": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
                "rightFoot": {"rightFoot": {"x": 0, "y": 0, "scaleX": 1, "scaleY": 1, "rotation": 0, "width": 50, "height": 5}},
            }
        },
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
        ("rightShoulder", 12, 14),
        ("rightUpperArm", 14, 16),
        ("rightElbow", 16, 16),
        ("rightForearm", 16, 18),
        ("rightHand", 18, 20),
        ("leftUpperLeg", 23, 25),
        ("leftKnee", 25, 25),
        ("leftLowerLeg", 25, 27),
        ("leftFoot", 27, 31),
        ("rightUpperLeg", 24, 26),
        ("rightKnee", 26, 26),
        ("rightLowerLeg", 26, 28),
        ("rightFoot", 28, 32),
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

            # Update attachment position and size based on landmarks
            if bone_name in spine_data["skins"]["default"]:
                attachment = spine_data["skins"]["default"][bone_name][bone_name]
                attachment["x"] = (start["x"] + end["x"]) / 2 - root_position["x"]
                attachment["y"] = (start["y"] + end["y"]) / 2 - root_position["y"]
                attachment["width"] = length
                attachment["height"] = length / 2

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