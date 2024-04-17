import os
import tkinter as tk
from PIL import Image, ImageTk
import shutil

class ImageClassifier:
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
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            image_width, image_height = self.image.size
            aspect_ratio = min(screen_width / image_width, screen_height / image_height)
            new_width = int(image_width * aspect_ratio)
            new_height = int(image_height * aspect_ratio)
            self.image = self.image.resize((new_width, new_height))
            self.photo = ImageTk.PhotoImage(self.image)
            self.label = tk.Label(self.master, image=self.photo)
            self.label.pack(fill=tk.BOTH, expand=tk.YES)
            classification = input(f"Press 1 for Art and 2 for Non-Art ").lower()
            if classification == "2":
                self.move_image_to_non_art(image_path)
            elif classification == "1":
                print("Image will remain in its original location.")
            else:
                print("Invalid classification. Skipping.")
            self.label.pack_forget()
            self.current_index += 1
            self.load_image()
        else:
            self.master.quit()

    def move_image_to_non_art(self, image_path):
        non_art_folder = os.path.join(os.path.dirname(image_path), "non_art")
        if not os.path.exists(non_art_folder):
            os.makedirs(non_art_folder)
        shutil.move(image_path, os.path.join(non_art_folder, os.path.basename(image_path)))

def classify_images_in_folder(folder_path):
    image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.lower().endswith(('.jpg', '.jpeg', '.png'))]
    root = tk.Tk()
    ImageClassifier(root, image_paths)

def main():
    folder_path = "X:\images"  # Adjust this path to your image folder
    classify_images_in_folder(folder_path)

if __name__ == "__main__":
    main()
