import tkinter as tk
from tkinter import messagebox
import random
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import Pillow modules

# Character pool with attributes
characters = [
    {
        "name": "Diluc",
        "weapon": "Claymore",
        "location": "Mondstadt",
        "affiliation": "Dawn Winery",
        "hair_color": "Red",
        "element": "Pyro",
        "height": "Tall",
    },
    {
        "name": "Xiangling",
        "weapon": "Polearm",
        "location": "Liyue",
        "affiliation": "Wanmin Restaurant",
        "hair_color": "Black",
        "element": "Pyro",
        "height": "Short",
    },
    {
        "name": "Kaeya",
        "weapon": "Sword",
        "location": "Mondstadt",
        "affiliation": "Knights of Favonius",
        "hair_color": "Blue",
        "element": "Cryo",
        "height": "Tall",
    },
    {
        "name": "Barbara",
        "weapon": "Catalyst",
        "location": "Mondstadt",
        "affiliation": "Church of Favonius",
        "hair_color": "Blonde",
        "element": "Hydro",
        "height": "Short",
    },
    {
        "name": "Razor",
        "weapon": "Claymore",
        "location": "Mondstadt",
        "affiliation": "Wolf Boy",
        "hair_color": "Silver",
        "element": "Electro",
        "height": "Medium",
    },
    # Add more characters as needed...
]

# Helper functions
def filter_by_attribute(attribute, value):
    return [char for char in characters if char.get(attribute) == value]

def true_random():
    return random.sample(characters, 4)

def competitive_random():
    # Placeholder for competitive logic, if needed
    return random.sample(characters, 4)

def character_select(character_name):
    for char in characters:
        if char["name"] == character_name:
            return char
    return None

# GUI Application
class GenshinRandomizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genshin Impact Randomizer")
        self.geometry("800x600")  # Increased size to accommodate icons
        self.resizable(False, False)
        self.frames = {}
        self.icon_dir = "icons"  # Directory for character icons
        self.character_images = self.load_character_images()
        self.setup_frames()

    def setup_frames(self):
        for F in (MainMenu, TrueRandomPage, CompRandomPage, MainSelectPage, AttributeSelectPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def load_character_images(self):
        """Load and resize character images from the icon directory."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(script_dir, "icons")

        images = {}
        for char in characters:
            filename = os.path.join(icon_dir, f"{char['name'].lower().replace(' ', '_')}.png")
            if os.path.exists(filename):
                # Open the image using Pillow and resize it
                pil_image = Image.open(filename).resize((64, 64), Image.Resampling.LANCZOS)
                images[char["name"]] = ImageTk.PhotoImage(pil_image)  # Convert to Tkinter-compatible format
            else:
                print(f"Warning: Missing icon for {char['name']} ({filename})")
                images[char["name"]] = None
        return images

# GUI Pages
class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Genshin Impact Randomizer", font=("Arial", 18)).pack(pady=20)
        tk.Button(self, text="True Random", command=lambda: master.show_frame(TrueRandomPage), width=20).pack(pady=10)
        tk.Button(self, text="Competitive Random", command=lambda: master.show_frame(CompRandomPage), width=20).pack(pady=10)
        tk.Button(self, text="Main Select", command=lambda: master.show_frame(MainSelectPage), width=20).pack(pady=10)
        tk.Button(self, text="Attribute Select", command=lambda: master.show_frame(AttributeSelectPage), width=20).pack(pady=10)

class TrueRandomPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="True Random Mode", font=("Arial", 18)).pack(pady=20)
        
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()
        
        team = true_random()
        for char in team:
            self.display_character(char["name"])

    def display_character(self, char_name):
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char_name)
        if icon:
            tk.Label(frame, image=icon).pack()
        tk.Label(frame, text=char_name, font=("Arial", 12)).pack()

class CompRandomPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Competitive Random Mode", font=("Arial", 18)).pack(pady=20)
        
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()
        
        team = competitive_random()
        for char in team:
            self.display_character(char["name"])

    def display_character(self, char_name):
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char_name)
        if icon:
            tk.Label(frame, image=icon).pack()
        tk.Label(frame, text=char_name, font=("Arial", 12)).pack()

class MainSelectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Main Select Mode", font=("Arial", 18)).pack(pady=20)
        
        tk.Label(self, text="Select a character:", font=("Arial", 14)).pack(pady=5)
        self.selected_char = tk.StringVar(value=characters[0]["name"])
        self.char_dropdown = tk.OptionMenu(self, self.selected_char, *[char["name"] for char in characters])
        self.char_dropdown.config(font=("Arial", 14), width=15)
        self.char_dropdown.pack(pady=5)
        
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()

        attribute = self.attribute.get()
        value = self.value.get()
        filtered_characters = filter_by_attribute(attribute, value)

        if filtered_characters:
            for char in filtered_characters:
                self.display_character(char["name"])
        else:
            tk.Label(self.team_frame, text=f"No characters match {attribute} = {value}.", font=("Arial", 14)).pack()

    def display_character(self, char_name):
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)

        icon = self.master.character_images.get(char_name)
        if icon:
            tk.Label(frame, image=icon).pack()
        tk.Label(frame, text=char_name, font=("Arial", 12)).pack()

class AttributeSelectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Attribute Select Mode", font=("Arial", 18)).pack(pady=20)

        # Select Attribute
        tk.Label(self, text="Select an attribute:", font=("Arial", 14)).pack(pady=5)
        self.attribute = tk.StringVar(value="element")
        self.attribute_dropdown = tk.OptionMenu(self, self.attribute, "element", "weapon", "hair_color", "location", "affiliation", "height")
        self.attribute_dropdown.config(font=("Arial", 14), width=15)
        self.attribute_dropdown.pack(pady=5)

        # Select Value
        tk.Label(self, text="Select a value:", font=("Arial", 14)).pack(pady=5)
        self.value = tk.StringVar(value="Pyro")
        self.value_dropdown = tk.OptionMenu(self, self.value, "Pyro", "Hydro", "Cryo", "Electro", "Claymore", "Polearm", "Catalyst", "Sword", "Tall", "Short", "Medium", "Mondstadt", "Liyue", "Dawn Winery", "Knights of Favonius", "Wanmin Restaurant", "Church of Favonius", "Wolf Boy")
        self.value_dropdown.config(font=("Arial", 14), width=15)
        self.value_dropdown.pack(pady=5)

        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)

        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()

        attribute = self.attribute.get()
        value = self.value.get()
        filtered_characters = filter_by_attribute(attribute, value)

        if filtered_characters:
            for char in filtered_characters:
                self.display_character(char["name"])
        else:
            tk.Label(self.team_frame, text=f"No characters match {attribute} = {value}.", font=("Arial", 14)).pack()

    def display_character(self, char_name):
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)

        icon = self.master.character_images.get(char_name)
        if icon:
            tk.Label(frame, image=icon).pack()
        tk.Label(frame, text=char_name, font=("Arial", 12)).pack()

if __name__ == "__main__":
    app = GenshinRandomizer()
    app.mainloop()
