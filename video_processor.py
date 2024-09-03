import cv2
import mediapipe as mp
import numpy as np
import json

class VideoProcessor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process_video(self, video_path, landmarks_output, overlay_video_output, skeleton_video_output, output_format):
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        landmarks_data = []

        # Set up video writers
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        overlay_out = cv2.VideoWriter(overlay_video_output, fourcc, fps, (width, height))
        skeleton_out = cv2.VideoWriter(skeleton_video_output, fourcc, fps, (width, height))

        for frame_num in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)
            
            if results.pose_landmarks:
                # Process landmarks based on the selected output format
                if output_format == "blender":
                    frame_data = {
                        "frame": frame_num,
                        "landmarks": [
                            {"x": lm.x, "y": lm.z, "z": -lm.y}  # Adjust for Blender's coordinate system
                            for lm in results.pose_landmarks.landmark
                        ]
                    }
                elif output_format == "spine":
                    frame_data = {
                        "frame": frame_num,
                        "landmarks": [
                            {"x": lm.x, "y": 1 - lm.y, "z": lm.z}  # Invert y-axis for Spine compatibility
                            for lm in results.pose_landmarks.landmark
                        ]
                    }
                else:
                    raise ValueError(f"Unsupported output format: {output_format}")

                landmarks_data.append(frame_data)

                # Draw the pose annotation on the frame
                self.mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                
                # Create a black image for the skeleton video
                black_frame = np.zeros((height, width, 3), dtype=np.uint8)
                self.mp_drawing.draw_landmarks(
                    black_frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                # Write the frames
                overlay_out.write(frame)
                skeleton_out.write(black_frame)

        cap.release()
        overlay_out.release()
        skeleton_out.release()

        # Save landmarks data to JSON
        with open(landmarks_output, 'w') as f:
            json.dump({"fps": fps, "frames": landmarks_data}, f)

    def draw_skeleton(self, frame, landmarks):
        # Helper function to draw lines between landmarks
        def draw_line(p1, p2, color=(0, 255, 0), thickness=2):
            cv2.line(frame, (int(p1.x * frame.shape[1]), int(p1.y * frame.shape[0])),
                     (int(p2.x * frame.shape[1]), int(p2.y * frame.shape[0])), color, thickness)

        # Draw main body lines
        draw_line(landmarks[11], landmarks[12])  # Shoulders
        draw_line(landmarks[11], landmarks[23])  # Left torso
        draw_line(landmarks[12], landmarks[24])  # Right torso
        draw_line(landmarks[23], landmarks[24])  # Hips

        # Draw arms
        draw_line(landmarks[11], landmarks[13])  # Left upper arm
        draw_line(landmarks[13], landmarks[15])  # Left lower arm
        draw_line(landmarks[12], landmarks[14])  # Right upper arm
        draw_line(landmarks[14], landmarks[16])  # Right lower arm

        # Draw legs
        draw_line(landmarks[23], landmarks[25])  # Left thigh
        draw_line(landmarks[25], landmarks[27])  # Left calf
        draw_line(landmarks[24], landmarks[26])  # Right thigh
        draw_line(landmarks[26], landmarks[28])  # Right calf

        # Draw head
        draw_line(landmarks[0], landmarks[11])  # Neck to left shoulder
        draw_line(landmarks[0], landmarks[12])  # Neck to right shoulder

# Usage
# processor = VideoProcessor()
# processor.process_video("input_video.mp4", "landmarks_output.json", "overlay_video.mp4", "skeleton_video.mp4")