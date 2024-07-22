import tkinter as tk
import subprocess
import os

def run_main():
    # Get the absolute path to the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the 'YoutubeTracker' folder if it exists
    yt_tracker_dir = os.path.join(current_dir, 'YoutubeTracker')
    if os.path.exists(yt_tracker_dir):
        os.chdir(yt_tracker_dir)
        subprocess.Popen(['python', 'main.py'])
    else:
        # Try to navigate from the parent directory
        parent_dir = os.path.dirname(current_dir)
        yt_tracker_dir = os.path.join(parent_dir, 'YoutubeTracker')
        if os.path.exists(yt_tracker_dir):
            os.chdir(yt_tracker_dir)
            subprocess.Popen(['python', 'main.py'])
        else:
            print("Error: 'YoutubeTracker' directory not found.")

def fetch_videos(channels):
    for channel_url in channels:
        fetch_script = os.path.join(os.path.dirname(__file__), 'fetch_youtube_videos.py')
        subprocess.Popen(['python', fetch_script, channel_url.strip()])

# List of YouTube channel URLs
channel_urls = [
    "https://www.youtube.com/@pawsvtuber/videos",
    "https://www.youtube.com/@Rosiebellmoo/videos",
    "https://www.youtube.com/@SmugAlanaVtuber/videos",
    "https://www.youtube.com/@NyaruSunako/videos"
    "https://www.youtube.com/@chelzorthedestroyer/videos"
    # Add more channel URLs as needed
]

# Create Tkinter window
root = tk.Tk()
root.title("YouTube Videos Tracker Splash")

# Label
label = tk.Label(root, text="Welcome to YouTube Videos Tracker", padx=20, pady=20)
label.pack()

# Button to run main.py
run_main_button = tk.Button(root, text="Run Main", command=run_main)
run_main_button.pack(pady=10)

# Button to fetch YouTube videos from all channels
fetch_videos_button = tk.Button(root, text="Fetch YouTube Videos", command=lambda: fetch_videos(channel_urls))
fetch_videos_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
