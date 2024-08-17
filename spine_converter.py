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
        "skeleton": {"hash": " ", "spine": "3.8.99", "width": 1000, "height": 1000},
        "bones": [
            {"name": "root"},
            {"name": "hip", "parent": "root"},
            {"name": "spine", "parent": "hip"},
            {"name": "chest", "parent": "spine"},
            {"name": "neck", "parent": "chest"},
            {"name": "head", "parent": "neck"},
            {"name": "leftShoulder", "parent": "chest"},
            {"name": "leftArm", "parent": "leftShoulder"},
            {"name": "leftForearm", "parent": "leftArm"},
            {"name": "rightShoulder", "parent": "chest"},
            {"name": "rightArm", "parent": "rightShoulder"},
            {"name": "rightForearm", "parent": "rightArm"},
            {"name": "leftUpLeg", "parent": "hip"},
            {"name": "leftLeg", "parent": "leftUpLeg"},
            {"name": "leftFoot", "parent": "leftLeg"},
            {"name": "rightUpLeg", "parent": "hip"},
            {"name": "rightLeg", "parent": "rightUpLeg"},
            {"name": "rightFoot", "parent": "rightLeg"}
        ],
        "slots": [],
        "skins": {"default": {}},
        "animations": {"animation": {"bones": {}}}
    }

    fps = data["fps"]
    frames = data["frames"]
    scale_factor = 1000  # Adjust this if needed

    for bone in spine_data["bones"]:
        spine_data["animations"]["animation"]["bones"][bone["name"]] = {"translate": [], "rotate": []}

    # Process first frame to set initial bone lengths
    first_frame = frames[0]["landmarks"]
    def get_pos(index):
        return {
            "x": first_frame[index]["x"] * scale_factor,
            "y": first_frame[index]["y"] * scale_factor  # No longer inverted
        }

    bone_data = [
        ("hip", 23, 24),
        ("spine", 23, 11),
        ("chest", 11, 12),
        ("neck", 12, 0),
        ("head", 0, 0),
        ("leftShoulder", 11, 13),
        ("leftArm", 13, 15),
        ("leftForearm", 15, 17),
        ("rightShoulder", 12, 14),
        ("rightArm", 14, 16),
        ("rightForearm", 16, 18),
        ("leftUpLeg", 23, 25),
        ("leftLeg", 25, 27),
        ("leftFoot", 27, 31),
        ("rightUpLeg", 24, 26),
        ("rightLeg", 26, 28),
        ("rightFoot", 28, 32)
    ]

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
                "y": landmarks[index]["y"] * scale_factor  # No longer inverted
            }

        hip_center = get_pos(23)  # Use left hip as center

        for bone_name, start_idx, end_idx in bone_data:
            start = get_pos(start_idx)
            end = get_pos(end_idx)
            angle = calculate_angle(start, end)
            
            spine_data["animations"]["animation"]["bones"][bone_name]["translate"].append({
                "time": time,
                "x": start["x"] - hip_center["x"],
                "y": start["y"] - hip_center["y"]
            })
            spine_data["animations"]["animation"]["bones"][bone_name]["rotate"].append({
                "time": time,
                "angle": angle
            })

        # Set root motion
        spine_data["animations"]["animation"]["bones"]["root"]["translate"].append({
            "time": time,
            "x": hip_center["x"],
            "y": hip_center["y"]
        })

    with open(output_file, 'w') as f:
        json.dump(spine_data, f, indent=2)

    print(f"Spine animation data saved to {output_file}")

# Usage
# convert_to_spine("landmarks_output.json", "spine_animation.json")