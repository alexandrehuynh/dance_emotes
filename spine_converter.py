import json

def convert_to_spine(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    spine_data = {
        "bones": [
            {"name": "root"},
            {"name": "body", "parent": "root"},
            {"name": "leftArm", "parent": "body"},
            {"name": "rightArm", "parent": "body"},
            {"name": "leftLeg", "parent": "root"},
            {"name": "rightLeg", "parent": "root"}
        ],
        "slots": [],
        "skins": {},
        "animations": {
            "animation1": {
                "bones": {
                    "body": {"translate": []},
                    "leftArm": {"translate": []},
                    "rightArm": {"translate": []},
                    "leftLeg": {"translate": []},
                    "rightLeg": {"translate": []}
                }
            }
        }
    }

    fps = data["fps"]
    frames = data["frames"]

    for frame in frames:
        frame_num = frame["frame"]
        time = frame_num / fps

        # Simplified mapping of MediaPipe landmarks to Spine bones
        spine_data["animations"]["animation1"]["bones"]["body"]["translate"].append({
            "time": time,
            "x": frame["landmarks"][11]["x"] * 100,  # Left shoulder
            "y": frame["landmarks"][11]["y"] * 100
        })
        
        # Add similar mappings for other bones (left/right arms and legs)
        # This is a simplified example and would need to be expanded for a full skeleton

    with open(output_file, 'w') as f:
        json.dump(spine_data, f, indent=2)

# Remove the following lines
# spine_file = convert_to_spine("landmarks_output.json", "spine_animation.json")
# print(f"Spine animation data saved to {spine_file}")