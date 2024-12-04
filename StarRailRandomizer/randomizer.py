import tkinter as tk
from tkinter import messagebox
import random
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import Pillow modules

# Character pool and competitive teams
characters = [
    "Raiden", "Argenti", "Aventurine", "Bailu", "Black Swan", "Blade", "Boothill", 
    "Bronya", "Clara", "Dan Heng - Imbibitor Lunae", "Dr. Ratio", "Feixiao", 
    "Firefly", "Fu Xuan", "Gepard", "Himeko", "Huohuo", "Jade", "Jiaoqiu", 
    "Jing Yuan", "Jingliu", "Kafka", "Lingsha", "Luocha", "Rappa", "Robin", 
    "Ruan Mei", "Seele", "Silver Wolf", "Sparkle", "Topaz", 
    "Trailblazer Fire", "Trailblazer Imaginary", "Trailblazer Physical", 
    "Welt", "Yanqing", "Yunli", "Arlan", "Asta", "Dan Heng", "Gallagher", 
    "Guinaifen", "Hanya", "Herta", "Hook", "Luka", "Lynx", "March 7th", 
    "March 7th Imaginary", "Misha", "Moze", "Natasha", "Pela", "Qingque", 
    "Sampo", "Serval", "Sushang", "Tingyun", "Xueyi", "Yukong", "Sunday"
]


competitive_teams = [
    #Raiden Teams
    ["Raiden", "Jiaoqiu", "Sparkle", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Fu Xuan"],
    ["Raiden", "Kafka", "Black Swan", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Huohuo"],
    ["Raiden", "Pela", "Sparkle", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Fu Xuan"],
    ["Raiden", "Pela", "Silver Wolf", "Fu Xuan"],
    ["Raiden", "Silver Wolf", "Sparkle", "Fu Xuan"],

    #Argenti
    ["Argenti", "Robin", "Tingyun", "Gallagher"],
    ["Jade", "Argenti", "Tingyun", "Aventurine"],
    ["Argenti", "Robin", "Sparkle", "Huohuo"],
    
    #Arlan has no teams lol
    
    #Asta
    ["Kafka", "Black Swan", "Asta", "Huohuo"],
    ["Firefly", "Asta", "Trailblazer Imaginary", "Lingsha"],
    ["Kafka", "Black Swan", "Asta", "Luocha"],
    ["Rappa", "Asta", "Ruan Mei", "Gallagher"],
    ["Himiko", "Asta", "Ruan Mei", "Aventurine"],
    ["Rappa", "Asta", "Trailblazer Imaginary", "Gallagher"],
    ["Firefly", "Asta", "Trailblazer Imaginary", "Gallagher"],
    ["Firefly", "Asta", "Trailblazer Imaginary", "Ruan Mei"],
    ["Kafka", "Black Swan", "Asta", "Bailu"],
    ["Rappa", "Asta", "Trailblazer Imaginary", "Lingsha"],
    
    #Adventurine
    


]

# Randomizer functions
def true_random():
    return random.sample(characters, 4)

def competitive_random():
    return random.choice(competitive_teams)

def character_select(character):
    valid_teams = [team for team in competitive_teams if character in team]
    if not valid_teams:
        return None
    return random.choice(valid_teams)

# GUI Application
class StarRailRandomizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Honkai: Star Rail Randomizer")
        self.geometry("600x400")  # Increased size to accommodate icons
        self.resizable(False, False)
        self.frames = {}
        self.icon_dir = "icons"  # Directory for character icons
        self.character_images = self.load_character_images()
        self.setup_frames()

    def setup_frames(self):
        for F in (MainMenu, TrueRandomPage, CompRandomPage, MainSelectPage):
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
            filename = os.path.join(icon_dir, f"{char.lower().replace(' ', '_')}.png")
            if os.path.exists(filename):
                # Open the image using Pillow and resize it
                pil_image = Image.open(filename).resize((64, 64), Image.Resampling.LANCZOS)  # Resize to 64x64
                images[char] = ImageTk.PhotoImage(pil_image)  # Convert to Tkinter-compatible format
            else:
                print(f"Warning: Missing icon for {char} ({filename})")
                images[char] = None
        return images



class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Honkai: Star Rail Randomizer", font=("Arial", 18)).pack(pady=20)
        tk.Button(self, text="True Random", command=lambda: master.show_frame(TrueRandomPage), width=20).pack(pady=10)
        tk.Button(self, text="Competitive Random", command=lambda: master.show_frame(CompRandomPage), width=20).pack(pady=10)
        tk.Button(self, text="Main Select", command=lambda: master.show_frame(MainSelectPage), width=20).pack(pady=10)

class TrueRandomPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="True Random Mode", font=("Arial", 18)).pack(pady=20)
        
        # Frame for displaying team icons and names
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()  # Clear previous team display
        
        team = true_random()
        for char in team:
            self.display_character(char)

    def display_character(self, char):
        """Display a character's icon and name."""
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char)
        if icon:
            tk.Label(frame, image=icon).pack()  # Display icon
        tk.Label(frame, text=char, font=("Arial", 12)).pack()  # Display name

class CompRandomPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Competitive Random Mode", font=("Arial", 18)).pack(pady=20)
        
        # Frame for displaying team icons and names
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()  # Clear previous team display
        
        team = competitive_random()
        for char in team:
            self.display_character(char)

    def display_character(self, char):
        """Display a character's icon and name."""
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char)
        if icon:
            tk.Label(frame, image=icon).pack()  # Display icon
        tk.Label(frame, text=char, font=("Arial", 12)).pack()  # Display name

class MainSelectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Main Select Mode", font=("Arial", 18)).pack(pady=20)
        
        tk.Label(self, text="Select a character:", font=("Arial", 14)).pack(pady=5)
        self.selected_char = tk.StringVar(value=characters[0])  # Default to the first character
        self.char_dropdown = tk.OptionMenu(self, self.selected_char, *characters)
        self.char_dropdown.config(font=("Arial", 14), width=15)
        self.char_dropdown.pack(pady=5)
        
        # Frame for displaying team icons and names
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        # Clear any existing team display
        for widget in self.team_frame.winfo_children():
            widget.destroy()

        # Get the selected character
        character = self.selected_char.get()
        team = character_select(character)
        
        if team:
            # Display each team member's icon and name
            for char in team:
                self.display_character(char)
        else:
            tk.Label(self.team_frame, text=f"No valid teams for {character}.", font=("Arial", 14)).pack()

    def display_character(self, char):
        """Display a character's icon and name."""
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char)
        if icon:
            tk.Label(frame, image=icon).pack()  # Display icon
        tk.Label(frame, text=char, font=("Arial", 12)).pack()  # Display name


# Run the application
if __name__ == "__main__":
    app = StarRailRandomizer()
    app.mainloop()
