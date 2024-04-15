import os
from PIL import Image, ImageTk
import tkinter as tk
import piexif

def add_tag_to_image(image_path, tag):
    try:
        # Load existing EXIF data from the image
        exif_data = piexif.load(image_path)
        
        # Get the existing tags from the EXIF data
        existing_tags_bytes = exif_data['0th'].get(piexif.ImageIFD.XPKeywords, b'')
        if isinstance(existing_tags_bytes, bytes):
            existing_tags = existing_tags_bytes.decode('utf-8')
        else:
            existing_tags = ''
        
        # Append the new tag to the existing tags
        updated_tags = existing_tags + (', ' if existing_tags else '') + tag
        
        # Encode the updated tags as bytes
        updated_tags_bytes = updated_tags.encode('utf-16le')
        
        # Update the EXIF data with the updated tags
        exif_data['0th'][piexif.ImageIFD.XPKeywords] = updated_tags_bytes
        
        # Convert the EXIF data back to binary format
        exif_bytes = piexif.dump(exif_data)
        
        # Save the modified EXIF data back to the image
        piexif.insert(exif_bytes, image_path)
        
        print(f"Tag '{tag}' added successfully to {image_path}")
    except Exception as e:
        print(f"Error adding tag to {image_path}: {e}")

def display_image(image_path):
    root = tk.Tk()
    root.title("Image Viewer")
    
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.pack()
    
    def on_close():
        root.destroy()
    
    button = tk.Button(root, text="Close", command=on_close)
    button.pack()
    
    root.mainloop()
    image.close()

def tag_images_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}")
            
            display_image(image_path)
            
            # Ask for a tag for this image
            tag = input("Enter a tag for this image (Press Enter to skip): ")
            if tag:
                add_tag_to_image(image_path, tag)

def main():
    folder_path = "C:/Users/joela/Desktop/test"  # Adjust this path to your image folder
    tag_images_in_folder(folder_path)

if __name__ == "__main__":
    main()
