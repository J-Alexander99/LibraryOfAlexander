import tkinter as tk
from tkinter import messagebox
import random
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Character pool with attributes
characters = [
    {"name": "Diluc", "weapon": "Claymore", "location": "Mondstadt", "affiliation": "Dawn Winery", "hair_color": "Red", "element": "Pyro", "height": "Tall"},
    {"name": "Xiangling", "weapon": "Polearm", "location": "Liyue", "affiliation": "Wanmin Restaurant", "hair_color": "Black", "element": "Pyro", "height": "Short"},
    {"name": "Kaeya", "weapon": "Sword", "location": "Mondstadt", "affiliation": "Knights of Favonius", "hair_color": "Blue", "element": "Cryo", "height": "Tall"},
    {"name": "Barbara", "weapon": "Catalyst", "location": "Mondstadt", "affiliation": "Church of Favonius", "hair_color": "Blonde", "element": "Hydro", "height": "Short"},
    {"name": "Razor", "weapon": "Claymore", "location": "Mondstadt", "affiliation": "Wolf Boy", "hair_color": "Silver", "element": "Electro", "height": "Medium"},

#4 Stars
    {"name": "", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},


#1.0s
    {"name": "Lumine`", "weapon": "Sword", "location": "Kahnria", "affiliation": "Knights Of Favonius", "hair_color": "Blonde", "element": "Dendro", "height": "Medium"},
    {"name": "Amber", "weapon": "Bow", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Brown", "element": "Pyro", "height": "Medium"},
    {"name": "Lisa", "weapon": "Catalyst", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Brown", "element": "Electro", "height": "Tall"},
    {"name": "Noelle", "weapon": "Claymore", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Silver", "element": "Geo", "height": "Medium"},
    {"name": "Kaeya", "weapon": "Sword", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Blue", "element": "Cryo", "height": "Tall"},
    {"name": "Barbara", "weapon": "Catalyst", "location": "Mondstat", "affiliation": "Chruch Of Favonius", "hair_color": "Blonde", "element": "Hydro", "height": "Medium"},
    {"name": "Diluc", "weapon": "Claymore", "location": "Mondstat", "affiliation": "Dawn Winary", "hair_color": "Red", "element": "Pyro", "height": "Tall"},
    {"name": "Jean", "weapon": "Sword", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Blonde", "element": "Anemo", "height": "Tall"},
    {"name": "Venti", "weapon": "Bow", "location": "Mondstat", "affiliation": "Dawn Winary", "hair_color": "Green", "element": "Anemo", "height": "Medium"},
    {"name": "Klee", "weapon": "Catalyst", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Blonde", "element": "Pyro", "height": "Short"},
    {"name": "Keqing", "weapon": "Sword", "location": "Liyue", "affiliation": "Millilith", "hair_color": "Purple", "element": "Electro", "height": "Medium"},
    {"name": "Qiqi", "weapon": "Sword", "location": "Liyue", "affiliation": "Farmacy", "hair_color": "Purple", "element": "Cryo", "height": "Short"},
    {"name": "Mona", "weapon": "Catalyst", "location": "Mondstat", "affiliation": "Witch", "hair_color": "Black", "element": "Hydro", "height": "Medium"},
    {"name": "Childe", "weapon": "Bow", "location": "Shnezia", "affiliation": "Fatui", "hair_color": "Ginger", "element": "Hydro", "height": "Tall"},
    {"name": "Zhongli", "weapon": "Polearm", "location": "Liyue", "affiliation": "Funural Parlor", "hair_color": "Brown", "element": "Geo", "height": "Tall"},
    {"name": "Albedo", "weapon": "Sword", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Blonde", "element": "Geo", "height": "Medium"},
    {"name": "Ganyu", "weapon": "Bow", "location": "Liyue", "affiliation": "Adeptus", "hair_color": "Blue", "element": "Cryo", "height": "Medium"},
    {"name": "Xiao", "weapon": "Polearm", "location": "Liyue", "affiliation": "Adeptus", "hair_color": "Green", "element": "Anemo", "height": "Medium"},
    {"name": "Hu Tao", "weapon": "Polearm", "location": "Liyue", "affiliation": "Funural Parler", "hair_color": "Brown", "element": "Pyro", "height": "Medium"},
    {"name": "Eula", "weapon": "Claymore", "location": "Mondstat", "affiliation": "Knights Of Favonius", "hair_color": "Blue", "element": "Cryo", "height": "Tall"},
    {"name": "Kazuha", "weapon": "Sword", "location": "Inazuma", "affiliation": "Watatsumi Island", "hair_color": "Blonde", "element": "Anemo", "height": "Medium"},

#2.0s
    {"name": "Ayaka", "weapon": "Sword", "location": "Inazuma", "affiliation": "Tenshaku", "hair_color": "Blue", "element": "Cryo", "height": "Medium"},
    {"name": "Yoimiya", "weapon": "Bow", "location": "Inazuma", "affiliation": "Fireworks Shop", "hair_color": "Red", "element": "Pyro", "height": "Medium"},
    {"name": "Raiden", "weapon": "Polearm", "location": "Inazuma", "affiliation": "Tenshaku", "hair_color": "Purple", "element": "Electro", "height": "Tall"},
    {"name": "Kokomi", "weapon": "Catalyst", "location": "Inazuma", "affiliation": "Watatsumi Island", "hair_color": "Blonde", "element": "Hydro", "height": "Medium"},
    {"name": "Itto", "weapon": "Claymore", "location": "Inazuma", "affiliation": "Arataki Gang", "hair_color": "White", "element": "Geo", "height": "Tall"},
    {"name": "Shenhe", "weapon": "Polearm", "location": "Liyue", "affiliation": "Adeptus", "hair_color": "White", "element": "Cryo", "height": "Tall"},
    {"name": "Yae Miko", "weapon": "Catalyst", "location": "Inazuma", "affiliation": "Shrine", "hair_color": "Pink", "element": "Electro", "height": "Tall"},
    {"name": "Ayato", "weapon": "Sword", "location": "Inazuma", "affiliation": "Tenshaku", "hair_color": "Blue", "element": "Hydro", "height": "Tall"},
    {"name": "Yelan", "weapon": "Bow", "location": "Liyue", "affiliation": "Millilith", "hair_color": "Blue", "element": "Hydro", "height": "Tall"},
    
#3.0
    {"name": "Tighnari", "weapon": "Bow", "location": "Sumeru", "affiliation": "Ranger", "hair_color": "Green", "element": "Dendro", "height": "Medium"},
    {"name": "Nilou", "weapon": "Sword", "location": "Sumeru", "affiliation": "Theature Group", "hair_color": "Red", "element": "Hydro", "height": "Medium"},
    {"name": "Cyno", "weapon": "Claymore", "location": "Sumeru", "affiliation": "University", "hair_color": "Black", "element": "Electro", "height": "Medium"},
    {"name": "Nahida", "weapon": "Catalyst", "location": "Sumeru", "affiliation": "University", "hair_color": "White", "element": "Dendro", "height": "Short"},
    {"name": "Wanderer", "weapon": "Catalyst", "location": "Sumeru", "affiliation": "University", "hair_color": "Black", "element": "Anemo", "height": "Medium"},
    {"name": "Alhaitham", "weapon": "Sword", "location": "Sumeru", "affiliation": "University", "hair_color": "Silver", "element": "Dendro", "height": "Tall"},
    {"name": "Deyah", "weapon": "Claymore", "location": "Sumeru", "affiliation": "Mercenary", "hair_color": "Brown", "element": "Pyro", "height": "Tall"},
    {"name": "Baizhu", "weapon": "Catalyst", "location": "Liyue", "affiliation": "Pharmacy", "hair_color": "Green", "element": "Dendro", "height": "Tall"},

#4.0s
    {"name": "Lynny", "weapon": "Bow", "location": "Fontaine", "affiliation": "Theatre Trope", "hair_color": "Blonde", "element": "Pyro", "height": "Medium"},
    {"name": "Neuvillette", "weapon": "Catalyst", "location": "Fontine", "affiliation": "Court Of Fontaine", "hair_color": "White", "element": "Hydro", "height": "Tall"},
    {"name": "Wriothesley", "weapon": "Catalyst", "location": "Fontaine", "affiliation": "Prison", "hair_color": "Black", "element": "Cryo", "height": "Tall"},
    {"name": "Furina", "weapon": "Sword", "location": "Fontaine", "affiliation": "Court Of Fontaine", "hair_color": "White", "element": "Hydro", "height": "Medium"},
    {"name": "Navia", "weapon": "Claymore", "location": "Fontaine", "affiliation": "Spina De La Rosula", "hair_color": "Blonde", "element": "Geo", "height": "Tall"},
    {"name": "Xianyun", "weapon": "Catalyst", "location": "Liyue", "affiliation": "Adeptus", "hair_color": "Green", "element": "Anemo", "height": "Tall"},
    {"name": "Chiori", "weapon": "Sword", "location": "Fontaine", "affiliation": "Chioria Boutique", "hair_color": "Brown", "element": "Geo", "height": "Medium"},
    {"name": "Arelecchino", "weapon": "Polearm", "location": "Shnezia", "affiliation": "Fatui", "hair_color": "White", "element": "Pyro", "height": "Tall"},
    {"name": "Clorinde", "weapon": "Sword", "location": "Fontaine", "affiliation": "Court Of Fontaine", "hair_color": "Blue", "element": "Electro", "height": "Tall"},
    {"name": "Seigwiene", "weapon": "Catalyst", "location": "Fontaine", "affiliation": "Fortress of Metropiede", "hair_color": "White", "element": "Hydro", "height": "Short"},
    {"name": "", "weapon": "Catalyst", "location": "Sumeru", "affiliation": "Florist", "hair_color": "Blonde", "element": "Dendro", "height": "Medium"},

#5.0s
    {"name": "Mualani", "weapon": "Catalyst", "location": "Natlan", "affiliation": "People Of Water", "hair_color": "White", "element": "Hydro", "height": "Medium"},
    {"name": "Kenich", "weapon": "Catalyst", "location": "Natlan", "affiliation": "", "hair_color": "Green", "element": "Dendro", "height": "Medium"},
    {"name": "Xilonen", "weapon": "Sword", "location": "Natlan", "affiliation": "", "hair_color": "Blonde", "element": "Geo", "height": "Tall"},
    {"name": "Chasca", "weapon": "Bow", "location": "Natlan", "affiliation": "", "hair_color": "Red", "element": "Anemo", "height": "Tall"},


    {"name": "Fischl", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Xiangling", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Xingqiu", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Sucrose", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Chongyun", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Diona", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Beidou", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Ningguang", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Razor", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Xinyan", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Bennett", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Rosaria", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Yanfei", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Sayu", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Kujou Sara", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Thoma", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Gorou", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Yun Jin", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Kuki Shinobu", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Heizou", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Collei", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Dori", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Candace", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Layla", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Faruzan", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Yaoyao", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Mika", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Kaveh", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Kirara", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Lynette", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Freminet", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Charlotte", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Chevreuse", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Gaming", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Sethos", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Kachina", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Ororon", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},
    {"name": "Lan Yan", "weapon": "", "location": "", "affiliation": "", "hair_color": "", "element": "", "height": ""},


]

# Predefined competitive teams
competitive_teams = [
    
    #Example Format
    ["Diluc", "Kaeya", "Barbara", "Xiangling"],
    ["Xiangling", "Razor", "Barbara", "Kaeya"],
    ["Diluc", "Xiangling", "Razor", "Kaeya"],
    # Add more teams as needed

    #Lumine

    #Amber

    #Diluc

    #Jean

    #Keqing

    #Mona

    #Qiqi

    #Venti

    #Klee

    #Childe

    #Zhongli

    #Albedo

    #Ganyu
    ["Ganyu", "Bennett", "Xiangling", "Zhongli"], #check this
    ["Ganyu", "Bennett", "Xiangling", "Kazuha"],
    ["Ganyu", "Xiangling", "Kazuha", "Zhongli"],
    ["Ganyu", "Xiangling", "Geo lady", "Kaeya"], #fix this

    #Xiao

    #Hu Tao
    ["Hu Tao", "Furina", "Yelan", "Xainyun"], #check this
    ["Hu Tao", "Furina", "Xingchio", "Kaeya"],


    #Eula
    ["Eula", "Yelan", "Yae Miko", "Zhongli"],

    #Kazuha


    #2.0

    #Ayaka

    #Yoimiya

    #Raiden

    #Kokomi

    #Itto

    #Shenhe

    #Yae Miko

    #Ayato

    #Yelan

#3.0

    #Tighnari

    #Nilou

    #Cyno

    #Nahida

    #Wanderer

    #Alhaitham

    #Deyah

    #Baizhu

#4.0

    #Lynny

    #Neuvillette

    #Wriosthlly

    #Furina

    #Navia

    #Xainyun

    #Chiori

    #Arelecchino

    #Clorinde 

    #Seigwiene

    #Emile
    
#5.0

    #Maulani

    #Kinich
    ["Kinich", "Bennett", "Emilie", "Xiangling"],
    ["Kinich", "Bennett", "Emilie", "Dehya"],
    ["Kinich", "Bennett", "Emilie", "Thoma"],
    ["Kinich", "Bennett", "Furina", "Xiangling"],
    ["Kinich", "Bennett", "Furina", "Dehya"],
    ["Kinich", "Bennett", "Furina", "Thoma"],
    ["Kinich", "Bennett", "Xiangling", "Albedo"],
    ["Kinich", "Bennett", "Xiangling", "Zhongli"],
    ["Kinich", "Bennett", "Xiangling", "Chiori"],
    ["Kinich", "Bennett", "Xingqiu", "Thoma"],
    
    #Geo Lady
    ["Neuvillette", "Furina", "Kazuha", "Xilonen"],
    ["Neuvillette", "Furina", "Lynette", "Xilonen"],
    ["Arlecchino", "Bennett", "Kazuha", "Xilonen"],
    ["Arlecchino", "Bennett", "Zhongli", "Xilonen"],
    ["Lyney", "Bennett", "Zhongli", "Xilonen"],
    ["Lyney", "Bennett", "Chiori", "Xilonen"],
    ["Wriothesley", "Shenhe", "Chiori", "Xilonen"],
    ["Ayato", "Furina", "Kazuha", "Xilonen"],
    ["Ayato", "Furina", "Yelan", "Xilonen"],
    ["Mualani", "Xiangling", "Sucrose", "Xilonen"],
    ["Maulani", "Xiangling", "Kazuha", "Xilonen"],
    ["Hu Tao", "Furina", "Yelan", "Xilonen"],
    ["Hu Tao", "Xingqiu", "Yelan", "Xilonen"],
    ["Neuvillette", "Xiangling", "Kazuha", "Xilonen"],
    ["Neuvillette", "Xiangling", "Emilie", "Xilonen"],
    ["Neuvillette", "Xiangling", "Lynette", "Xilonen"],
    ["Wriothesley", "Bennett", "Xiangling", "Xilonen"],
    ["Ayaka", "Furina", "Shenhe", "Xilonen"],
    ["Wriothesley", "Furina", "Yelan", "Xilonen"],
    ["Wriothesley", "Furina", "Shenhe", "Xilonen"],
    ["CLorinde", "Fischl", "Kirara", "Xilonen"],
    ["CLorinde", "Fischl", "Nahida", "Xilonen"],
    ["Cyno", "Furina", "Nahida", "Xilonen"],
    ["Cyno", "Fischl", "Nahida", "Xilonen"],
    ["Navia", "Fischl", "Bennett", "Xilonen"],
    ["Navia", "Furina", "Bennett", "Xilonen"],
    ["Navia", "Xiangling", "Bennett", "Xilonen"],
    ["Noelle", "Furina", "Yelan", "Xilonen"],

    #Chasca
    ["Chasca", "Bennett", "Furina", "Xilonen"],
    ["Chasca", "Bennett", "Furina", "Zhongli"],
    ["Chasca", "Bennett", "Furina", "Kazuha"],
    ["Chasca", "Bennett", "Furina", "Xiangling"],
    ["Chasca", "Bennett", "Furina", "Diona"],
    ["Chasca", "Bennett", "Furina", "Shenhe"],
    ["Chasca", "Bennett", "Furina", "Layla"],
    ["Chasca", "Bennett", "Mona", "Xiangling"],
    ["Chasca", "Bennett", "Rosaria", "Xiangling"],
    ["Chasca", "Bennett", "Furina", "Ororon"],
    ["Chasca", "Bennett", "Furina", "Chevreuse"],
    ["Chasca", "Bennett", "Furina", "Fischl"],
    ["Chasca", "Bennett", "Furina", "Beidou"],
    ["Chasca", "Bennett", "Furina", "Sara"],
    ["Chasca", "Fischl", "Yaoyao", "Yae Miko"],
    ["Chasca", "Shenhe", "Charlotte", "Furina"],
    ["Chasca", "Sigewinne", "Furina", "Ororon"],
    ["Chasca", "Furina", "Ororon", "Baizhu"],


]

def filter_by_attribute(attribute, value):
    return [team for team in competitive_teams if all(char[attribute] == value for char in characters if char["name"] in team)]

def filter_by_main_character(character_name):
    return [team for team in competitive_teams if character_name in team]

def true_random():
    return random.sample(characters, 4)

def select_from_list(teams):
    return random.choice(teams) if teams else None

class GenshinRandomizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genshin Impact Randomizer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.frames = {}
        self.icon_dir = "icons"
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(script_dir, "icons")
        images = {}
        for char in characters:
            filename = os.path.join(icon_dir, f"{char['name'].lower().replace(' ', '_')}.png")
            if os.path.exists(filename):
                pil_image = Image.open(filename).resize((64, 64), Image.Resampling.LANCZOS)
                images[char["name"]] = ImageTk.PhotoImage(pil_image)
            else:
                print(f"Warning: Missing icon for {char['name']} ({filename})")
                images[char["name"]] = None
        return images

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
        team = select_from_list(competitive_teams)
        if team:
            for char in team:
                self.display_character(char)

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
        selected_char = self.selected_char.get()
        teams = filter_by_main_character(selected_char)
        team = select_from_list(teams)
        if team:
            for char in team:
                self.display_character(char)
        else:
            tk.Label(self.team_frame, text=f"No teams contain {selected_char}.", font=("Arial", 14)).pack()

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
        tk.Label(self, text="Select an attribute:", font=("Arial", 14)).pack(pady=5)
        self.attribute = tk.StringVar(value="element")
        self.attribute_dropdown = tk.OptionMenu(self, self.attribute, "element", "weapon", "location", "affiliation", "height")
        self.attribute_dropdown.config(font=("Arial", 14), width=15)
        self.attribute_dropdown.pack(pady=5)
        tk.Label(self, text="Select a value:", font=("Arial", 14)).pack(pady=5)
        self.value = tk.StringVar(value="Pyro")
        self.value_dropdown = tk.OptionMenu(self, self.value, "Pyro", "Hydro", "Cryo", "Electro", "Claymore", "Polearm", "Catalyst", "Sword", "Tall", "Short", "Medium", "Mondstadt", "Liyue")
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
        teams = filter_by_attribute(attribute, value)
        team = select_from_list(teams)
        if team:
            for char in team:
                self.display_character(char)
        else:
            tk.Label(self.team_frame, text=f"No teams match {attribute} = {value}.", font=("Arial", 14)).pack()

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
