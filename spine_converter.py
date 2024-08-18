import json
import math

def calculate_angle(a, b):
    return math.degrees(math.atan2(b['y'] - a['y'], b['x'] - a['x']))

def calculate_length(a, b):
    return math.sqrt((b['x'] - a['x'])**2 + (b['y'] - a['y'])**2)

def create_line_attachment(bone_name, length):
    return {
        bone_name: {
            "line": {
                "name": "line",
                "path": "images/line.png",
                "x": 0,
                "y": 0,
                "scaleX": length / 100,
                "scaleY": 1,
                "width": 100,
                "height": 5
            }
        }
    }

def convert_to_spine(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    spine_data = {
        "skeleton": {"hash": " ", "spine": "4.2.35", "width": 1000, "height": 1000},
        "bones": [
            {"name": "root"},
            {"name": "leftHip", "parent": "root"},
            {"name": "rightHip", "parent": "root"},
            {"name": "spine", "parent": "root"},
            {"name": "chest", "parent": "spine"},
            {"name": "neck", "parent": "chest"},
            {"name": "head", "parent": "neck"},
            {"name": "leftShoulder", "parent": "chest"},
            {"name": "leftUpperArm", "parent": "leftShoulder"},
            {"name": "leftLowerArm", "parent": "leftUpperArm"},
            {"name": "leftHand", "parent": "leftLowerArm"},
            {"name": "rightShoulder", "parent": "chest"},
            {"name": "rightUpperArm", "parent": "rightShoulder"},
            {"name": "rightLowerArm", "parent": "rightUpperArm"},
            {"name": "rightHand", "parent": "rightLowerArm"},
            {"name": "leftUpperLeg", "parent": "leftHip"},
            {"name": "leftLowerLeg", "parent": "leftUpperLeg"},
            {"name": "leftFoot", "parent": "leftLowerLeg"},
            {"name": "rightUpperLeg", "parent": "rightHip"},
            {"name": "rightLowerLeg", "parent": "rightUpperLeg"},
            {"name": "rightFoot", "parent": "rightLowerLeg"}
        ],
        "slots": [],
        "skins": {"default": {}},
        "animations": {"animation": {"bones": {}}}
    }

    fps = data["fps"]
    frames = data["frames"]
    scale_factor = 500

    for bone in spine_data["bones"]:
        spine_data["animations"]["animation"]["bones"][bone["name"]] = {"translate": [], "rotate": [], "scale": []}

    # Process first frame to set initial bone lengths
    first_frame = frames[0]["landmarks"]
    def get_pos(index):
        return {
            "x": first_frame[index]["x"] * scale_factor,
            "y": first_frame[index]["y"] * scale_factor
        }

    bone_data = [
        ("leftHip", 23, 24),
        ("rightHip", 24, 23),
        ("spine", 23, 11),
        ("chest", 11, 12),
        ("neck", 12, 0),
        ("head", 0, 0),
        ("leftShoulder", 11, 13),
        ("leftUpperArm", 13, 15),
        ("leftLowerArm", 15, 17),
        ("leftHand", 17, 19),
        ("rightShoulder", 12, 14),
        ("rightUpperArm", 14, 16),
        ("rightLowerArm", 16, 18),
        ("rightHand", 18, 20),
        ("leftUpperLeg", 23, 25),
        ("leftLowerLeg", 25, 27),
        ("leftFoot", 27, 31),
        ("rightUpperLeg", 24, 26),
        ("rightLowerLeg", 26, 28),
        ("rightFoot", 28, 32)
    ]

    # Set initial bone positions and lengths
    for bone_name, start_idx, end_idx in bone_data:
        start = get_pos(start_idx)
        end = get_pos(end_idx)
        length = calculate_length(start, end)
        for bone in spine_data["bones"]:
            if bone["name"] == bone_name:
                bone["length"] = length
                bone["x"] = end["x"] - start["x"]
                bone["y"] = end["y"] - start["y"]
                break

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

        for bone_name, start_idx, end_idx in bone_data:
            start = get_pos(start_idx)
            end = get_pos(end_idx)
            
            angle = calculate_angle(start, end)
            length = calculate_length(start, end)
            original_length = next(bone["length"] for bone in spine_data["bones"] if bone["name"] == bone_name)
            scale = length / original_length if original_length != 0 else 1
            
            spine_data["animations"]["animation"]["bones"][bone_name]["translate"].append({
                "time": time,
                "x": start["x"] - root_position["x"],
                "y": start["y"] - root_position["y"]
            })
            spine_data["animations"]["animation"]["bones"][bone_name]["rotate"].append({
                "time": time,
                "angle": angle
            })
            spine_data["animations"]["animation"]["bones"][bone_name]["scale"].append({
                "time": time,
                "x": scale,
                "y": scale
            })

        # Set root motion
        spine_data["animations"]["animation"]["bones"]["root"]["translate"].append({
            "time": time,
            "x": root_position["x"],
            "y": root_position["y"]
        })

    # Add slots and attachments
    spine_data["slots"] = [{"name": bone["name"], "bone": bone["name"], "attachment": "line"} for bone in spine_data["bones"]]
    
    for bone in spine_data["bones"]:
        if "length" in bone:
            spine_data["skins"]["default"].update(create_line_attachment(bone["name"], bone["length"]))

    # Add the image to the Spine JSON
    spine_data["skeleton"]["images"] = "./images/"

    with open(output_file, 'w') as f:
        json.dump(spine_data, f, indent=2)

    print(f"Spine animation data saved to {output_file}")

# Usage
# convert_to_spine("landmarks_output.json", "spine_animation.json")