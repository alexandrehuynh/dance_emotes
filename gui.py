import os
import tkinter as tk
import datetime
from tkinter import filedialog, messagebox, ttk
from video_processor import VideoProcessor
from spine_converter import convert_to_spine
from blender_converter import generate_blender_script
from landmark_visualizer import visualize_landmarks

class VideoConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Video to Animation Converter")
        master.geometry("400x300")

        self.label = tk.Label(master, text="Select a video file to process:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Video", command=self.select_file)
        self.select_button.pack(pady=10)

        self.conversion_type = tk.StringVar(value="blender")
        self.radio_frame = ttk.Frame(master)
        self.radio_frame.pack(pady=10)

        self.blender_radio = ttk.Radiobutton(self.radio_frame, text="Blender", variable=self.conversion_type, value="blender")
        self.blender_radio.pack(side=tk.LEFT, padx=10)

        self.spine_radio = ttk.Radiobutton(self.radio_frame, text="Spine", variable=self.conversion_type, value="spine")
        self.spine_radio.pack(side=tk.LEFT, padx=10)

        self.process_button = tk.Button(master, text="Process Video", command=self.process_video, state=tk.DISABLED)
        self.process_button.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=10)

        self.input_video = None

    def select_file(self):
        self.input_video = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if self.input_video:
            self.status_label.config(text=f"Selected: {os.path.basename(self.input_video)}")
            self.process_button.config(state=tk.NORMAL)

    def process_video(self):
        if not self.input_video:
            messagebox.showerror("Error", "No video file selected.")
            return

        # Create timestamped output directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_name = os.path.splitext(os.path.basename(self.input_video))[0]
        
        output_format = self.conversion_type.get()
        base_output_dir = f"output_{output_format}"
        output_dir = os.path.join(base_output_dir, f"{video_name}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        # Define output paths
        landmarks_output = os.path.join(output_dir, "landmarks.json")
        overlay_video_output = os.path.join(output_dir, "overlay_video.mp4")
        skeleton_video_output = os.path.join(output_dir, "skeleton_video.mp4")

        # Process video
        self.status_label.config(text="Processing video...")
        self.master.update()
        
        processor = VideoProcessor()
        try:
            processor.process_video(self.input_video, landmarks_output, overlay_video_output, skeleton_video_output, output_format)
            self.status_label.config(text="Video processing complete.")
            self.master.update()
        except Exception as e:
            messagebox.showerror("Error", f"Error processing video: {e}")
            return

        # Visualize landmarks
        self.status_label.config(text="Generating landmark visualizations...")
        self.master.update()
        visualize_landmarks(landmarks_output, output_dir)

        # Convert based on selected type
        self.status_label.config(text=f"Converting to {output_format} format...")
        self.master.update()
        
        if output_format == "spine":
            spine_output = os.path.join(output_dir, "spine_animation.json")
            convert_to_spine(landmarks_output, spine_output)
            self.status_label.config(text="Spine conversion complete!")
        else:  # Blender
            blender_script = os.path.join(output_dir, "blender_conversion_script.py")
            blender_output = os.path.join(output_dir, "blender_animation.blend")
            script_path = generate_blender_script(landmarks_output, blender_output)
            self.status_label.config(text="Blender script generated. Please run it in Blender.")
            instructions = (
                f"A Blender script has been generated at {blender_script}.\n\n"
                "To use this script:\n"
                "1. Open Blender\n"
                "2. Go to Scripting workspace\n"
                "3. Open the generated script in the Text Editor\n"
                "4. In Blender's Python Console, run the following command:\n"
                f"   exec(compile(open('{script_path}').read(), '{script_path}', 'exec'))\n"
                "5. Wait for the script to finish running\n"
                "6. The animation will be imported and saved as a new Blender file"
            )
            messagebox.showinfo("Blender Conversion Instructions", instructions)

        self.status_label.config(text="Process complete!")
        messagebox.showinfo("Success", f"Processing complete!\nOutputs saved in: {output_dir}")

def main():
    root = tk.Tk()
    app = VideoConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()