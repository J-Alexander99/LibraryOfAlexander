from PIL import Image
import os
import shutil

def get_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = width / height
        return aspect_ratio

def sort_photos_by_aspect_ratio(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of image files in input directory
    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # Sort image files by aspect ratio
    sorted_files = sorted(image_files, key=lambda x: get_aspect_ratio(os.path.join(input_dir, x)))

    # Organize files into subdirectories based on aspect ratio
    current_aspect_ratio = None
    current_subdir = None
    for filename in sorted_files:
        aspect_ratio = get_aspect_ratio(os.path.join(input_dir, filename))
        if aspect_ratio != current_aspect_ratio:
            current_aspect_ratio = aspect_ratio
            current_subdir = os.path.join(output_dir, f"{aspect_ratio:.2f}")
            os.makedirs(current_subdir, exist_ok=True)
        src_path = os.path.join(input_dir, filename)
        dst_path = os.path.join(current_subdir, filename)
        shutil.move(src_path, dst_path)
        print(f"Moved {filename} to {current_subdir}")

if __name__ == "__main__":
    input_directory = "C:\\Users\\joela\\Desktop\\test"
    output_directory = "C:\\Users\\joela\\Desktop\\test\\sorted"
    sort_photos_by_aspect_ratio(input_directory, output_directory)
