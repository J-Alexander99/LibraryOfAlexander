import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk  # Import from Pillow

class CDLMapDraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CDL Map Draft")

        self.team_a = None
        self.team_b = None
        self.current_team = None
        self.map_pools = {
            "Hardpoint": ["Skyline", "Vault", "Hacienda", "Protocol", "Red Card"],
            "Search and Destroy": ["Skyline", "Red Card", "Hacienda", "Protocol", "Vault"],
            "Control": ["Hacienda", "Protocol", "Vault"]
        }
        self.draft_results = {
            "Hardpoint": [],
            "Search and Destroy": [],
            "Control": []
        }
        self.final_map_series = []
        self.map_images = {
            "Skyline": "images/skyline.webp",
            "Vault": "images/vault.webp",
            "Hacienda": "images/hacienda.webp",
            "Protocol": "images/protocol.webp",
            "Red Card": "images/RedCard.webp"
        }
        self.setup_ui()

    def setup_ui(self):
        self.team1_label = tk.Label(self.root, text="Enter the name of Team 1:")
        self.team1_label.pack()
        self.team1_entry = tk.Entry(self.root)
        self.team1_entry.pack()

        self.team2_label = tk.Label(self.root, text="Enter the name of Team 2:")
        self.team2_label.pack()
        self.team2_entry = tk.Entry(self.root)
        self.team2_entry.pack()

        self.start_button = tk.Button(self.root, text="Start Draft", command=self.start_draft)
        self.start_button.pack()

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

    def start_draft(self):
        team1 = self.team1_entry.get().strip()
        team2 = self.team2_entry.get().strip()

        if not team1 or not team2:
            messagebox.showerror("Error", "Please enter names for both teams.")
            return

        self.team_a, self.team_b = random.sample([team1, team2], 2)
        self.current_team = self.team_a

        messagebox.showinfo("Coin Flip Result", f"{self.team_a} is Team A, {self.team_b} is Team B.")
        self.start_hardpoint_phase()

    def start_hardpoint_phase(self):
        self.current_phase = "Hardpoint"
        self.available_maps = self.map_pools[self.current_phase][:]
        self.draft_results[self.current_phase] = []
        self.ban_or_pick_map(f"{self.current_team}, choose a map to ban:")

    def ban_or_pick_map(self, prompt):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        tk.Label(self.options_frame, text=prompt).pack()

        for map_name in self.available_maps:
            button = tk.Button(
                self.options_frame, text=map_name, 
                command=lambda m=map_name: self.handle_map_choice(m)
            )
            button.pack(pady=2)

    def handle_map_choice(self, choice):
        if len(self.draft_results[self.current_phase]) < 2:  # Banning phase
            self.available_maps.remove(choice)
            self.draft_results[self.current_phase].append((self.current_team, "ban", choice))
            self.switch_team()

            if len(self.draft_results[self.current_phase]) < 2:
                self.ban_or_pick_map(f"{self.current_team}, choose a map to ban:")
            else:
                self.pick_map(f"{self.current_team}, choose the map for {self.current_phase}:")
        else:  # Picking phase
            self.draft_results[self.current_phase].append((self.current_team, "pick", choice))
            self.final_map_series.append((self.current_phase, choice))
            self.available_maps.remove(choice)
            self.switch_team()

            if self.current_phase == "Hardpoint":
                if len(self.draft_results[self.current_phase]) == 4:
                    self.start_snd_phase()
                else:
                    self.pick_map(f"{self.current_team}, choose the next Hardpoint map:")
            elif self.current_phase == "Search and Destroy":
                if len(self.draft_results[self.current_phase]) == 4:
                    self.start_control_phase()
                else:
                    self.pick_map(f"{self.current_team}, choose the next Search and Destroy map:")
            elif self.current_phase == "Control":
                self.display_final_results()

    def pick_map(self, prompt):
        self.ban_or_pick_map(prompt)

    def switch_team(self):
        self.current_team = self.team_a if self.current_team == self.team_b else self.team_b

    def start_snd_phase(self):
        self.current_phase = "Search and Destroy"
        self.available_maps = self.map_pools[self.current_phase][:]
        self.draft_results[self.current_phase] = []
        self.ban_or_pick_map(f"{self.current_team}, choose a map to ban:")

    def start_control_phase(self):
        self.current_phase = "Control"
        self.available_maps = self.map_pools[self.current_phase][:]
        self.draft_results[self.current_phase] = []
        self.ban_or_pick_map(f"{self.current_team}, choose a map to ban:")

    def display_final_results(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        tk.Label(self.options_frame, text="**Final Map Series**").pack()

        series_frame = tk.Frame(self.options_frame)
        series_frame.pack()

        for phase, map_name in self.final_map_series:
            map_frame = tk.Frame(series_frame)
            map_frame.pack(side=tk.LEFT, padx=10)

            # Using Pillow to open and display the image
            img = Image.open(self.map_images[map_name])
            img = img.resize((100, 100))  # Resize the image
            map_image = ImageTk.PhotoImage(img)

            map_label = tk.Label(map_frame, image=map_image)
            map_label.image = map_image
            map_label.pack()

            tk.Label(map_frame, text=f"{phase}: {map_name}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CDLMapDraftApp(root)
    root.mainloop()
