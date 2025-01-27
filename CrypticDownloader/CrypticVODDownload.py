import os
import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL
from PIL import Image, ImageTk

def download_video():
    link = link_entry.get()
    if not link.strip():
        messagebox.showerror("Error", "Please enter a valid YouTube link.")
        return
    
    try:
        # Get the directory of the executable
        executable_dir = os.path.dirname(os.path.abspath(__file__))

        # Define the path for the Downloads folder relative to the executable directory
        downloads_folder = os.path.join(executable_dir, "Downloads")

        # Create the Downloads folder if it doesn't exist
        os.makedirs(downloads_folder, exist_ok=True)

        # Set yt-dlp options to download video
        ydl_opts = {
            'format': 'best',  # Download the best video+audio format available
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Save with title and extension
        }

        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            downloaded_file = ydl.prepare_filename(info)
            messagebox.showinfo("Download Complete", f"Video downloaded and saved as: {downloaded_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Cryptic YouTube Downloader")

# Set window size and position
window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Configure window background color
root.configure(bg="#121212")

# Load the icon using relative path
executable_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(executable_dir, "images", "favicon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)

# Load the image using relative path
image_path = os.path.join(executable_dir, "images", "bronya.jpg")
if os.path.exists(image_path):
    image = Image.open(image_path)
    image = image.resize((200, 200))
    img = ImageTk.PhotoImage(image)
else:
    img = None

# Create label for the image
if img:
    image_label = tk.Label(root, image=img, bg="#121212")
    image_label.image = img
    image_label.pack()

# Create label and entry for the link
link_label = tk.Label(root, text="Enter YouTube Link:", fg="#C0C0C0", bg="#121212", font=("Arial", 12))
link_label.pack()
link_entry = tk.Entry(root, width=60, bd=3, relief=tk.FLAT, bg="#2E2E2E", fg="#C0C0C0", font=("Arial", 12))
link_entry.pack()

# Create download button
download_button = tk.Button(root, text="Download", command=download_video, bg="#008080", fg="#FFFFFF", font=("Arial", 12), relief=tk.RAISED)
download_button.pack(pady=10)

# Run the application
root.mainloop()
