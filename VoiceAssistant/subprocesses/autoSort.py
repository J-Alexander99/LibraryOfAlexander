import os
import shutil
import glob
import re

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r'[\/:*?"<>|]', '', filename)

def organize_downloads(downloads_folder, sorted_folder):
    # Check if the "sorted" folder exists on the desktop, if not, create one
    sorted_path = os.path.join(os.path.expanduser("~"), "Desktop", sorted_folder)
    if not os.path.exists(sorted_path):
        os.makedirs(sorted_path)

    # Get a list of all files in the downloads folder
    download_files = glob.glob(os.path.join(downloads_folder, '*'))

    # Create folders for images, videos, and audio
    images_folder = os.path.join(sorted_path, "Images")
    videos_folder = os.path.join(sorted_path, "Videos")
    audio_folder = os.path.join(sorted_path, "Audio")

    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)

    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    # Loop through each file and move it to the corresponding folder in "sorted"
    for file_path in download_files:
        try:
            if os.path.isfile(file_path):
                file_type = file_path.split('.')[-1].lower()  # Get the file extension
                dest_folder = None

                # Determine destination folder based on file type
                if file_type in ["jpg", "jpeg", "png", "gif", "bmp"]:
                    dest_folder = images_folder
                elif file_type in ["mp4", "avi", "mkv", "mov"]:
                    dest_folder = videos_folder
                elif file_type in ["mp3", "wav", "ogg", "flac"]:
                    dest_folder = audio_folder

                # If the file type is neither image, video, nor audio, create a folder for it
                if dest_folder is None:
                    dest_folder_name = sanitize_filename(file_type)
                    dest_folder = os.path.join(sorted_path, dest_folder_name)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)

                # Move the file to the destination folder
                shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))

        except Exception as e:
            print(f"Error processing file: {file_path}\nError details: {str(e)}")

if __name__ == "__main__":
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    sorted_folder = "sorted"

    organize_downloads(downloads_folder, sorted_folder)
