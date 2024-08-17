import json
import math

def calculate_angle(a, b):
    return math.degrees(math.atan2(b['y'] - a['y'], b['x'] - a['x']))

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
    scale_factor = 500  # Adjust this as needed

    for bone in spine_data["bones"]:
        spine_data["animations"]["animation"]["bones"][bone["name"]] = {"translate": [], "rotate": []}

    for frame in frames:
        frame_num = frame["frame"]
        time = frame_num / fps
        landmarks = frame["landmarks"]

        def get_pos(index):
            return {
                "x": landmarks[index]["x"] * scale_factor,
                "y": landmarks[index]["y"] * scale_factor  # No longer inverted
            }

        # Map MediaPipe landmarks to Spine bones
        hip = get_pos(23)  # Left hip as center
        spine = get_pos(11)  # Left shoulder
        neck = get_pos(0)  # Nose
        left_shoulder = get_pos(11)
        left_elbow = get_pos(13)
        left_wrist = get_pos(15)
        right_shoulder = get_pos(12)
        right_elbow = get_pos(14)
        right_wrist = get_pos(16)
        left_hip = get_pos(23)
        left_knee = get_pos(25)
        left_ankle = get_pos(27)
        right_hip = get_pos(24)
        right_knee = get_pos(26)
        right_ankle = get_pos(28)

        # Calculate and set positions and rotations
        bone_data = [
            ("hip", hip, spine),
            ("spine", spine, neck),
            ("neck", spine, neck),
            ("head", neck, get_pos(0)),
            ("leftShoulder", spine, left_shoulder),
            ("leftArm", left_shoulder, left_elbow),
            ("leftForearm", left_elbow, left_wrist),
            ("rightShoulder", spine, right_shoulder),
            ("rightArm", right_shoulder, right_elbow),
            ("rightForearm", right_elbow, right_wrist),
            ("leftUpLeg", hip, left_knee),
            ("leftLeg", left_knee, left_ankle),
            ("leftFoot", left_ankle, get_pos(31)),
            ("rightUpLeg", hip, right_knee),
            ("rightLeg", right_knee, right_ankle),
            ("rightFoot", right_ankle, get_pos(32))
        ]

        for bone_name, start, end in bone_data:
            angle = calculate_angle(start, end)
            spine_data["animations"]["animation"]["bones"][bone_name]["translate"].append({
                "time": time,
                "x": start["x"] - hip["x"],
                "y": start["y"] - hip["y"]
            })
            spine_data["animations"]["animation"]["bones"][bone_name]["rotate"].append({
                "time": time,
                "angle": angle
            })

        # Set root motion
        spine_data["animations"]["animation"]["bones"]["root"]["translate"].append({
            "time": time,
            "x": hip["x"],
            "y": hip["y"]
        })

    with open(output_file, 'w') as f:
        json.dump(spine_data, f, indent=2)

    print(f"Spine animation data saved to {output_file}")

# Usage
# convert_to_spine("landmarks_output.json", "spine_animation.json")