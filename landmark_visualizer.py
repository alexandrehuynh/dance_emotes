import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def visualize_landmarks(landmarks_file, output_dir):
    # Load the landmark data
    with open(landmarks_file, 'r') as f:
        data = json.load(f)

    frames = data['frames']
    
    # Create a directory for the visualizations
    vis_dir = os.path.join(output_dir, 'landmark_visualizations')
    os.makedirs(vis_dir, exist_ok=True)

    # Create visualizations for the first, middle, and last frames
    frame_indices = [0, len(frames) // 2, -1]
    
    for idx in frame_indices:
        frame = frames[idx]
        landmarks = frame['landmarks']
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        xs = [lm['x'] for lm in landmarks]
        ys = [lm['y'] for lm in landmarks]
        zs = [lm['z'] for lm in landmarks]
        
        ax.scatter(xs, ys, zs)
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Frame {frame["frame"]}')
        
        # Save the plot
        plt.savefig(os.path.join(vis_dir, f'frame_{frame["frame"]}_visualization.png'))
        plt.close()

    print(f"Landmark visualizations saved in {vis_dir}")

# This function will be called from gui.py