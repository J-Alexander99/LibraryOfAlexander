import os
import ctypes
import platform
import random
from PIL import Image
#NEEDS BUGFIXING THIS DOES NOT WORK YET AND HAS NOT BEEN TESTED
def set_wallpaper(image_path, monitor_number=1):
    if platform.system() == 'Windows':
        SPI_SETDESKWALLPAPER = 0x0014
        MONITOR_DEFAULTTONEAREST = 0x00000002

        # Convert image path to Windows format
        image_path = os.path.abspath(image_path)
        image_path = image_path.replace('/', '\\')

        # Load the image
        image = Image.open(image_path)

        # Determine screen width and height
        width, height = image.size

        # Get handle to the desktop window
        hdesktop = ctypes.windll.user32.GetDesktopWindow()

        # Set the wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

        # Update the desktop
        ctypes.windll.user32.UpdatePerUserSystemParameters(1)

# Specify the paths to the folders for each monitor
folder_paths = {
    1: '/path/to/first/monitor/folder/',
    2: '/path/to/second/monitor/folder/',
    3: '/path/to/third/monitor/folder/',
    4: '/path/to/fourth/monitor/folder/'
}

# Assign random wallpapers to each monitor
for monitor_number, folder_path in folder_paths.items():
    # Get a list of image files in the folder
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('jpeg', 'jpg', 'png', 'bmp'))]
    
    # Select a random image file from the folder
    if image_files:
        random_image = random.choice(image_files)
        set_wallpaper(random_image, monitor_number)
    else:
        print(f"No image files found in {folder_path} for monitor {monitor_number}")
