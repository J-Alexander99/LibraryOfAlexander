import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
from PIL import Image, ImageTk

def convert_mp3_to_wav(mp3_file, output_file):
    command = ["ffmpeg", "-i", mp3_file, "-acodec", "pcm_s16le", "-ar", "44100", output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        mp3_entry.delete(0, tk.END)
        mp3_entry.insert(0, file_path)

def transfigure():
    mp3_file = mp3_entry.get()
    output_format = format_var.get()

    if mp3_file and output_format:
        output_file = os.path.splitext(mp3_file)[0] + "." + output_format
        convert_mp3_to_wav(mp3_file, output_file)
        result_label.config(text=f"File converted and saved as {output_file}")
    else:
        result_label.config(text="Please select an MP3 file and output format.")

# Create the main window
root = tk.Tk()
root.title("MP3 Transfigure")
root.configure(background='#333333')  # Set background color to dark grey

# Get the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the image relative to the script directory
image_path = os.path.join(script_dir, "images", "record.webp")
if os.path.exists(image_path):
    image = Image.open(image_path)
    image = image.resize((200, 200))
    img = ImageTk.PhotoImage(image)
else:
    img = None

# Style configurations
style = ttk.Style()
style.theme_use('clam')  # Choose a theme
style.configure('Gold.TButton', background='#FFD700', foreground='black', font=('Helvetica', 12, 'bold'))
style.configure('Purple.TButton', background='#800080', foreground='white', font=('Helvetica', 12, 'bold'))
style.configure('TLabel', foreground='white', font=('Helvetica', 12))

# Add the image to the window
if img:
    image_label = tk.Label(root, image=img, bg='#333333')  # Set background color to dark grey
    image_label.pack()

# Add a button to select the MP3 file
select_button = ttk.Button(root, text="Select MP3 File", command=select_file, style='Gold.TButton')
select_button.pack()

# Add an entry to display the selected MP3 file path
mp3_entry = ttk.Entry(root, width=50)
mp3_entry.pack()

# Add a dropdown box for selecting the output format
formats = ["wav", "ogg", "flac", "m4a"]
format_var = tk.StringVar(root)
format_var.set(formats[0])
format_menu = ttk.OptionMenu(root, format_var, *formats)
format_menu.pack()

# Add a button to start the conversion process
transfigure_button = ttk.Button(root, text="Transfigure", command=transfigure, style='Purple.TButton')
transfigure_button.pack()

# Add a label to display the conversion result
result_label = ttk.Label(root, text="", style='TLabel')
result_label.pack()

root.mainloop()
