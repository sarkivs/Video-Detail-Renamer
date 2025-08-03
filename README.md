Video Metadata Renamer

A simple yet powerful Python GUI application for Windows that automatically scans a folder of videos and renames them by appending their resolution and bitrate to the filename.

Do you have a folder full of video files with generic names? This tool helps you organize your video library by providing key technical information at a glance, directly in the filename. The Video Metadata Renamer scans each video, detects its resolution (e.g., 1920x1080) and bitrate (e.g., 5500kbps), and renames the file accordingly.

For example, a file named project-final-v2.mp4 can be automatically renamed to project-final-v2_1920x1080_5500kbps.mp4.

How It Works

The application is built using Python's standard tkinter library for the GUI. When a user selects a folder, the script iterates through the files and identifies common video formats (e.g., .mp4, .mkv, .avi).

For each video, it runs a ffprobe command in the background as a subprocess. ffprobe is a powerful command-line tool from the FFmpeg project that can analyze multimedia streams. The script requests the video's width, height, and bit_rate in JSON format, which is then parsed to extract the necessary information.

Finally, it constructs the new filename and uses Python's os module to rename the file on the disk. The entire process is run in a separate thread to ensure the GUI remains responsive.

Prerequisites :

FFmpeg: You must have FFmpeg installed on your Windows system and, crucially, have its bin folder added to your system's PATH. The script relies on being able to call ffprobe from any command-line location.

You can download FFmpeg from the official website: ffmpeg.org

For instructions on adding a directory to your PATH, see this helpful guide.

How to Use

Clone or Download the Repository:

Generated bash
git clone https://github.com/your-username/video-metadata-renamer.git
cd video-metadata-renamer


Or download the video_renamer.py script directly.

Run the Script:
Make sure you have Python installed, then run the application from your terminal:

Generated bash
python video_renamer.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Select a Folder:
Click the "Browse Folder" button and navigate to the directory containing the videos you wish to rename.

Let it Run:
The application will automatically start processing the files. You can monitor the progress in the log window. The "Browse Folder" button will be disabled during processing and will become active again once the task is complete.

Supported Video Formats

The script is configured to look for the following file extensions:
.mp4, .mkv, .avi, .mov, .flv, .wmv

You can easily add more extensions by modifying the video_extensions list in the script.

Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request.
