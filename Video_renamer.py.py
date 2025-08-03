import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
import subprocess
import json
from threading import Thread

class VideoRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Renamer")
        self.root.geometry("600x400")

        self.label = tk.Label(root, text="Select a folder containing videos to rename.")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse Folder", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.log_area.pack(pady=10, padx=10)

        self.add_log("Welcome to Video Renamer!\n")
        self.add_log("This script requires FFmpeg to be installed and in your system's PATH.\n")
        self.add_log("You can download FFmpeg from https://ffmpeg.org/\n")


    def add_log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.add_log(f"Selected folder: {folder_path}")
            self.browse_button.config(state=tk.DISABLED)
            # Run the renaming process in a separate thread to keep the GUI responsive
            thread = Thread(target=self.rename_videos_in_folder, args=(folder_path,))
            thread.start()

    def get_video_metadata(self, file_path):
        try:
            ffprobe_cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,bit_rate',
                '-of', 'json',
                file_path
            ]
            result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)
            if metadata.get('streams') and len(metadata['streams']) > 0:
                stream = metadata['streams'][0]
                width = stream.get('width')
                height = stream.get('height')
                bitrate = stream.get('bit_rate')
                return width, height, bitrate
        except FileNotFoundError:
            self.add_log("Error: ffprobe not found. Please make sure FFmpeg is installed and in your system's PATH.")
            return None, None, None
        except subprocess.CalledProcessError as e:
            self.add_log(f"Error processing {os.path.basename(file_path)} with ffprobe: {e.stderr}")
            return None, None, None
        except json.JSONDecodeError:
            self.add_log(f"Error decoding JSON from ffprobe for {os.path.basename(file_path)}")
            return None, None, None
        return None, None, None


    def rename_videos_in_folder(self, folder_path):
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']
        files_renamed = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in video_extensions):
                self.add_log(f"Processing: {filename}")
                width, height, bitrate = self.get_video_metadata(file_path)

                if width and height and bitrate:
                    try:
                        bitrate_in_kbps = int(bitrate) // 1000
                        resolution = f"{width}x{height}"
                        name, ext = os.path.splitext(filename)
                        new_name = f"{name}_{resolution}_{bitrate_in_kbps}kbps{ext}"
                        new_file_path = os.path.join(folder_path, new_name)

                        if os.path.exists(new_file_path):
                            self.add_log(f"Skipping rename, '{new_name}' already exists.")
                            continue

                        os.rename(file_path, new_file_path) # [1, 3, 5, 9, 12]
                        self.add_log(f"  -> Renamed to: {new_name}")
                        files_renamed += 1
                    except Exception as e:
                        self.add_log(f"  -> Error renaming file: {e}")
                else:
                    self.add_log(f"  -> Could not retrieve metadata for {filename}.")

        self.add_log(f"\nFinished processing. Renamed {files_renamed} video(s).")
        self.browse_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoRenamerApp(root)
    root.mainloop()