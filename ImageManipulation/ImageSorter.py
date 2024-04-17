from PIL import Image
import os
import shutil

def get_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = width / height
        return aspect_ratio

def categorize_aspect_ratio(aspect_ratio):
    # Define aspect ratio boundaries
    if aspect_ratio < 0.5:
        return "Ultratall"
    elif aspect_ratio < 0.75:
        return "Tall"
    elif aspect_ratio < 1.25:
        return "Square"
    elif aspect_ratio < 1.5:
        return "Wide"
    elif aspect_ratio < 2.1:
        return "Desktop"
    elif aspect_ratio < 2.4:
        return "Ultrawide"
    else:
        return "Unrecognisable"

def sort_photos_by_aspect_ratio(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of image files in input directory
    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # Organize files into subdirectories based on categorized aspect ratio
    for filename in image_files:
        aspect_ratio = get_aspect_ratio(os.path.join(input_dir, filename))
        category = categorize_aspect_ratio(aspect_ratio)
        category_dir = os.path.join(output_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        src_path = os.path.join(input_dir, filename)
        dst_path = os.path.join(category_dir, filename)
        shutil.move(src_path, dst_path)
        print(f"Moved {filename} to {category_dir}")

if __name__ == "__main__":
    input_directory = "C:\\Users\\joela\\Desktop\\test"
    output_directory = "C:\\Users\\joela\\Desktop\\test"
    sort_photos_by_aspect_ratio(input_directory, output_directory)
