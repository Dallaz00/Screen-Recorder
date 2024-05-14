import tkinter as tk
import time
import pyautogui
import threading
import numpy as np
import cv2
from tkinter import messagebox


class ScreenRecording:
    def __init__(self, _root):
        self.recording_thread = None
        self.root = _root
        self.root.title("Screen Recording")

        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(_root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.time_label = tk.Label(_root, text=" ", font=("Nunito", 12))
        self.time_label.pack(pady=10)

        self.recording = False
        self.start_time = 0
        self.video_writer = None
    
    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.start_time = time.time()
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.recording_thread.join()  # will wait for the recording to finish

        # check if the video_writer object has been initialized
        if self.video_writer is not None:
            self.video_writer.release()

        elapsed_time = time.time() - self.start_time
        print(f"Recording Duration: {elapsed_time:.2f} seconds")
        self.time_label.config(text="Recording stopped")

        self.save_video()

    def record_screen(self):
        screen_width, screen_height = pyautogui.size()
        try:
            self.video_writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20, (screen_width, screen_height))
        except Exception as e:
            print(f"Error initializing video writer: {e}")
            self.video_writer = None
            return

        while self.recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            try:
                self.video_writer.write(frame)
            except Exception as e:
                print(f"Error writing frame to video writer: {e}")
                self.video_writer = None
                return

            elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"Recording time: {elapsed_time:.2f} seconds")
            self.time_label.update()

    def save_video(self):
        # rename the recorded file with a timestamp
        current_time = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"{current_time}.avi"
        try:
            import os
            os.rename("output.avi", file_name)
            print(f"Video saved as {file_name}")
            messagebox.showinfo("Video Saved", f"Video saved as {file_name}")
        except Exception as e:
            print(f"Failed to save video: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecording(root)
    root.mainloop()
