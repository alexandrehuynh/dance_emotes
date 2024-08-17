import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from video_processor import VideoProcessor
from spine_converter import convert_to_spine

class VideoToSpineConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Video to Spine Converter")
        master.geometry("400x250")

        self.label = tk.Label(master, text="Select a video file to process:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Video", command=self.select_file)
        self.select_button.pack(pady=10)

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

        # Create output directory
        output_dir = "output_" + os.path.splitext(os.path.basename(self.input_video))[0]
        os.makedirs(output_dir, exist_ok=True)

        # Define output paths
        landmarks_output = os.path.join(output_dir, "landmarks.json")
        spine_output = os.path.join(output_dir, "spine_animation.json")
        overlay_video_output = os.path.join(output_dir, "overlay_video.mp4")
        skeleton_video_output = os.path.join(output_dir, "skeleton_video.mp4")

        # Process video
        self.status_label.config(text="Processing video...")
        self.master.update()
        
        processor = VideoProcessor()
        try:
            processor.process_video(self.input_video, landmarks_output, overlay_video_output, skeleton_video_output)
            self.status_label.config(text="Video processing complete.")
            self.master.update()
        except cv2.error as e:
            messagebox.showerror("Error", f"Error processing video: {e}\nThis might be due to an unsupported video codec or corrupt file.")
            return

        # Convert to Spine format
        self.status_label.config(text="Converting to Spine format...")
        self.master.update()
        
        convert_to_spine(landmarks_output, spine_output)
        
        self.status_label.config(text="Process complete!")
        messagebox.showinfo("Success", f"Processing complete!\nOutputs saved in: {output_dir}")

def main():
    root = tk.Tk()
    app = VideoToSpineConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()