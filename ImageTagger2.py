import os
import tkinter as tk
from PIL import Image, ImageTk
import piexif

class ImageTagger:
    def __init__(self, master, image_paths):
        self.master = master
        self.image_paths = image_paths
        self.current_index = 0
        
        self.load_image()
        self.master.attributes('-fullscreen', True)
        
        self.master.mainloop()
        
    def load_image(self):
        if self.current_index < len(self.image_paths):
            image_path = self.image_paths[self.current_index]
            self.image = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.label = tk.Label(self.master, image=self.photo)
            self.label.pack(fill=tk.BOTH, expand=tk.YES)
            tag = input(f"Enter a tag for {image_path} (Press Enter to skip): ")
            if tag:
                add_tag_to_image(image_path, tag)
                self.current_index += 1
                self.label.pack_forget()
                self.load_image()
            else:
                self.label.pack_forget()
                self.current_index += 1
                self.load_image()
        else:
            self.master.quit()

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

def tag_images_in_folder(folder_path):
    image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.lower().endswith(('.jpg', '.jpeg', '.png'))]
    root = tk.Tk()
    ImageTagger(root, image_paths)

def main():
    folder_path = "C:/Users/joela/Desktop/test"  # Adjust this path to your image folder
    tag_images_in_folder(folder_path)

if __name__ == "__main__":
    main()
