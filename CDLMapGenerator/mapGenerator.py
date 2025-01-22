import random
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk

# Define the map generation logic
def generate_cdl_map_set():
    # Define the map pool for each mode
    hardpoint_maps = ["Skyline", "Vault", "Hacienda", "Protocol", "Red Card"]
    snd_maps = ["Skyline", "Red Card", "Hacienda", "Protocol", "Vault"]
    control_maps = ["Hacienda", "Protocol", "Vault"]

    # Initialize an empty map set
    map_set = []

    # Generate maps for each mode in the specified order
    gamemode_order = ["Hardpoint", "Search and Destroy", "Control", "Hardpoint", "Search and Destroy"]
    used_maps = {"Hardpoint": set(), "Search and Destroy": set(), "Control": set()}

    for gamemode in gamemode_order:
        if gamemode == "Hardpoint":
            available_maps = list(set(hardpoint_maps) - used_maps["Hardpoint"])
        elif gamemode == "Search and Destroy":
            available_maps = list(set(snd_maps) - used_maps["Search and Destroy"])
        elif gamemode == "Control":
            available_maps = list(set(control_maps) - used_maps["Control"])

        # Randomly select a map from the available pool
        selected_map = random.choice(available_maps)
        map_set.append((gamemode, selected_map))

        # Mark the selected map as used for the current mode
        used_maps[gamemode].add(selected_map)

    return map_set

# Define the UI
def generate_map_set_ui():
    # Generate the map set
    map_set = generate_cdl_map_set()

    # Clear the frame and display the results
    for widget in result_frame.winfo_children():
        widget.destroy()

    for idx, (mode, map_name) in enumerate(map_set, start=1):
        # Adjust the filename for special cases and construct the file path
        filename = map_name.replace(" ", "") if map_name == "Red Card" else map_name
        image_path = os.path.join("images", f"{filename}.webp")

        try:
            # Load the map icon if it exists
            pil_image = Image.open(image_path)

            # Resize image to fit within a maximum width and height (based on 3840x2160)
            max_width, max_height = 250, 250  # Set maximum size for the images

            # Calculate new size while maintaining aspect ratio
            pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # Convert the image to PhotoImage
            icon = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Error loading image for {map_name}: {e}")
            # Use a placeholder if the image is not found
            icon = PhotoImage(width=100, height=100)

        # Create a frame for each map
        map_frame = tk.Frame(result_frame, padx=10, pady=10, bg="#ff77ff", bd=2, relief="solid", borderwidth=1)
        map_frame.pack(side=tk.LEFT, padx=15, pady=15)

        # Display the icon
        icon_label = tk.Label(map_frame, image=icon, bg="#ff77ff")
        icon_label.image = icon  # Keep a reference to avoid garbage collection
        icon_label.pack()

        # Display the map name
        map_label = tk.Label(map_frame, text=f"{mode}\n{map_name}", font=("Helvetica", 12), fg="#fff", bg="#ff77ff", justify=tk.CENTER)
        map_label.pack()

def show_about():
    messagebox.showinfo("About", "CDL Map Set Generator\nCreated with Python and Tkinter")

# Create the main application window
app = tk.Tk()
app.title("CDL Map Set Generator")

# Set the background color and window size (3840x2160 for large resolution)
app.configure(bg="#2b2b2b")
app.geometry("3840x2160")  # Large window size

# Create and place widgets
header_label = tk.Label(app, text="CDL Map Set Generator", font=("Arial", 24, "bold"), fg="#ff77ff", bg="#2b2b2b")
header_label.pack(pady=30)

instructions_label = tk.Label(app, text="Click the button below to generate a random map set.", font=("Arial", 16), fg="#fff", bg="#2b2b2b")
instructions_label.pack(pady=15)

# Generate button with hover effect
def on_enter(e):
    generate_button.config(bg="#ff40ff")

def on_leave(e):
    generate_button.config(bg="#ff77ff")

generate_button = tk.Button(app, text="Generate Map Set", font=("Arial", 16), bg="#ff77ff", fg="white", command=generate_map_set_ui)
generate_button.pack(pady=25)
generate_button.bind("<Enter>", on_enter)
generate_button.bind("<Leave>", on_leave)

# Frame to display the results
result_frame = tk.Frame(app, bg="#2b2b2b")
result_frame.pack(pady=30)

# Menu bar
menu_bar = tk.Menu(app)
app.config(menu=menu_bar)

# Add an About menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Run the application
app.mainloop()
