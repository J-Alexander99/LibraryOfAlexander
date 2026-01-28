import os
from PIL import Image
from pathlib import Path

def reduce_image_size(input_folder, output_folder, quality=85, max_size=None):
    """
    Reduce image file sizes while preserving quality.
    
    Args:
        input_folder: Path to folder containing original images
        output_folder: Path to folder where reduced images will be saved
        quality: JPEG quality (1-100), default 85 for good balance
        max_size: Optional tuple (width, height) to resize images if needed
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    # Process each file in the input folder
    processed_count = 0
    total_original_size = 0
    total_reduced_size = 0
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Skip if not a file
        if not os.path.isfile(file_path):
            continue
        
        # Check if the file is a supported image format
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in supported_formats:
            continue
        
        try:
            # Open the image
            with Image.open(file_path) as img:
                # Convert RGBA to RGB if saving as JPEG
                if img.mode == 'RGBA' and file_ext in {'.jpg', '.jpeg'}:
                    # Create a white background
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3])  # 3 is the alpha channel
                    img = rgb_img
                elif img.mode not in ('RGB', 'L'):
                    # Convert other modes to RGB
                    img = img.convert('RGB')
                
                # Resize if max_size is specified
                if max_size:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Prepare output path with same filename
                output_path = os.path.join(output_folder, filename)
                
                # Convert PNG to JPG for better compression (optional)
                if file_ext == '.png':
                    output_path = os.path.splitext(output_path)[0] + '.jpg'
                
                # Save with optimization
                if file_ext in {'.jpg', '.jpeg'} or (file_ext == '.png' and output_path.endswith('.jpg')):
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                elif file_ext == '.png':
                    img.save(output_path, 'PNG', optimize=True)
                else:
                    img.save(output_path, optimize=True)
                
                # Track file sizes
                original_size = os.path.getsize(file_path)
                reduced_size = os.path.getsize(output_path)
                total_original_size += original_size
                total_reduced_size += reduced_size
                
                reduction_percent = ((original_size - reduced_size) / original_size) * 100
                
                print(f"✓ {filename}: {original_size/1024:.1f}KB → {reduced_size/1024:.1f}KB ({reduction_percent:.1f}% reduction)")
                processed_count += 1
                
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Processed {processed_count} images")
    print(f"Total original size: {total_original_size/1024/1024:.2f} MB")
    print(f"Total reduced size: {total_reduced_size/1024/1024:.2f} MB")
    if total_original_size > 0:
        total_reduction = ((total_original_size - total_reduced_size) / total_original_size) * 100
        print(f"Overall reduction: {total_reduction:.1f}%")
    print(f"{'='*60}")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Configuration - folders in same directory as script
    INPUT_FOLDER = os.path.join(script_dir, "input")
    OUTPUT_FOLDER = os.path.join(script_dir, "output")
    
    # Quality setting (1-100): higher = better quality but larger file size
    # 85 is a good balance between quality and file size
    QUALITY = 85
    
    # Optional: Set maximum dimensions (width, height)
    # Uncomment and adjust if you want to resize images
    # MAX_SIZE = (1920, 1080)
    MAX_SIZE = None
    
    print("Image Size Reducer")
    print("="*60)
    print(f"Input folder: {INPUT_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    print(f"Quality: {QUALITY}")
    print(f"Max size: {MAX_SIZE or 'Original size'}")
    print("="*60)
    print()
    
    # Check if input folder exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Input folder '{INPUT_FOLDER}' does not exist!")
        print("Please create the folder and add your images, or update INPUT_FOLDER path.")
    else:
        reduce_image_size(INPUT_FOLDER, OUTPUT_FOLDER, quality=QUALITY, max_size=MAX_SIZE)
        print("\nDone! Check the output folder for processed images.")
