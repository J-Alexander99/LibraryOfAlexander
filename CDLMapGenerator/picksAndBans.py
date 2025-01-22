import tkinter as tk
from tkinter import messagebox
import random

class MapDraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CDL Map Draft")
        self.root.geometry("600x700")

        # Team Names
        self.team_1 = None
        self.team_2 = None

        # Maps
        self.hardpoint_maps = ["Skyline", "Vault", "Hacienda", "Protocol", "Red Card"]
        self.snd_maps = ["Skyline", "Red Card", "Hacienda", "Protocol", "Vault"]
        self.control_maps = ["Hacienda", "Protocol", "Vault"]

        # Draft Data
        self.draft_result = {}

        # Initialize State
        self.phase = None
        self.available_maps = None
        self.team_a = None
        self.team_b = None

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Team Names
        self.team_name_label = tk.Label(self.root, text="Enter Team Names", font=("Arial", 14))
        self.team_name_label.pack(pady=10)

        self.team_1_entry = tk.Entry(self.root, font=("Arial", 12))
        self.team_1_entry.pack(pady=5)
        self.team_1_entry.insert(0, "Team 1 Name")

        self.team_2_entry = tk.Entry(self.root, font=("Arial", 12))
        self.team_2_entry.pack(pady=5)
        self.team_2_entry.insert(0, "Team 2 Name")

        self.start_button = tk.Button(self.root, text="Start Draft", font=("Arial", 14), command=self.start_draft)
        self.start_button.pack(pady=20)

        # Display area for draft process
        self.draft_display = tk.Text(self.root, width=50, height=15, font=("Arial", 12), wrap=tk.WORD)
        self.draft_display.pack(pady=10)
        self.draft_display.config(state=tk.DISABLED)

    def start_draft(self):
        self.team_1 = self.team_1_entry.get().strip()
        self.team_2 = self.team_2_entry.get().strip()

        if not self.team_1 or not self.team_2:
            messagebox.showerror("Error", "Please enter both team names.")
            return

        self.draft_result.clear()
        self.draft_display.config(state=tk.NORMAL)
        self.draft_display.delete(1.0, tk.END)

        # Coin flip
        coin_flip = random.choice([self.team_1, self.team_2])
        team_a = self.team_1 if coin_flip == self.team_1 else self.team_2
        team_b = self.team_2 if team_a == self.team_1 else self.team_1

        self.draft_result["Team A"] = team_a
        self.draft_result["Team B"] = team_b

        self.draft_display.insert(tk.END, f"Coin flip result: {team_a} is Team A, {team_b} is Team B\n\n")

        # Start with Hardpoint phase
        self.phase = "Hardpoint"
        self.available_maps = self.hardpoint_maps[:]
        self.team_a = team_a
        self.team_b = team_b

        self.draft_display.insert(tk.END, "**Hardpoint Map Phase**\n")
        self.draft_display.insert(tk.END, f"{team_a}, choose a map to ban.\n")
        self.draft_display.config(state=tk.DISABLED)

        self.show_map_buttons(self.available_maps)

    def show_map_buttons(self, maps):
        """Display available maps as buttons and handle selection."""
        if hasattr(self, 'map_buttons_frame'):
            for widget in self.map_buttons_frame.winfo_children():
                widget.destroy()
        
        self.map_buttons_frame = tk.Frame(self.root)
        self.map_buttons_frame.pack(pady=10)

        for map_name in maps:
            button = tk.Button(self.map_buttons_frame, text=map_name, font=("Arial", 12),
                               command=lambda m=map_name: self.select_map(m))
            button.pack(pady=2, padx=5, fill=tk.X)

    def select_map(self, selected_map):
        """Handle the map selection by removing it and updating the draft result."""
        if self.phase == "Hardpoint":
            self.handle_phase_action(selected_map, "ban")
        elif self.phase == "Search and Destroy":
            self.handle_phase_action(selected_map, "ban")
        elif self.phase == "Control":
            self.handle_phase_action(selected_map, "ban")

    def handle_phase_action(self, selected_map, action):
        """Process a map ban or pick action."""
        if action == "ban":
            # Store the ban in the draft result
            self.draft_result[f"{self.team_a} Ban"] = selected_map
            self.available_maps.remove(selected_map)
            self.draft_display.config(state=tk.NORMAL)
            self.draft_display.insert(tk.END, f"{self.team_a} bans: {selected_map}\n")
            self.draft_display.config(state=tk.DISABLED)

            # Remove the map buttons
            for widget in self.map_buttons_frame.winfo_children():
                widget.destroy()

            # Switch teams for the next phase
            self.team_a, self.team_b = self.team_b, self.team_a

            # If all bans are done, proceed with picks
            if len(self.draft_result) < 2:  # Check for 2 bans
                self.draft_display.config(state=tk.NORMAL)
                self.draft_display.insert(tk.END, f"{self.team_a} picks the map.\n")
                self.draft_display.config(state=tk.DISABLED)
                self.show_map_buttons(self.available_maps)

            else:
                # Update phase and map lists
                self.next_phase()

    def next_phase(self):
        """Move to the next phase (Search and Destroy or Control)."""
        if self.phase == "Hardpoint":
            self.phase = "Search and Destroy"
            self.available_maps = self.snd_maps[:]
            self.draft_display.config(state=tk.NORMAL)
            self.draft_display.insert(tk.END, "\n**Search and Destroy Map Phase**\n")
            self.draft_display.insert(tk.END, f"{self.team_a}, choose a map to ban.\n")
            self.draft_display.config(state=tk.DISABLED)
            self.show_map_buttons(self.available_maps)
        elif self.phase == "Search and Destroy":
            self.phase = "Control"
            self.available_maps = self.control_maps[:]
            self.draft_display.config(state=tk.NORMAL)
            self.draft_display.insert(tk.END, "\n**Control Map Phase**\n")
            self.draft_display.insert(tk.END, f"{self.team_a}, choose a map to ban.\n")
            self.draft_display.config(state=tk.DISABLED)
            self.show_map_buttons(self.available_maps)
        elif self.phase == "Control":
            self.draft_display.config(state=tk.NORMAL)
            self.draft_display.insert(tk.END, "\n**Draft Complete**\n")
            self.draft_display.insert(tk.END, f"Final Draft:\n")
            self.draft_display.insert(tk.END, f"Map 1 (Hardpoint): {self.draft_result.get(f'{self.team_a} Ban')}\n")
            self.draft_display.insert(tk.END, f"Map 2 (Search and Destroy): {self.draft_result.get(f'{self.team_b} Ban')}\n")
            self.draft_display.insert(tk.END, f"Map 3 (Control): {self.draft_result.get(f'{self.team_a} Ban')}\n")
            self.draft_display.insert(tk.END, f"Map 4 (Hardpoint): {self.draft_result.get(f'{self.team_b} Ban')}\n")
            self.draft_display.insert(tk.END, f"Map 5 (Search and Destroy): {self.draft_result.get(f'{self.team_a} Ban')}\n")
            self.draft_display.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MapDraftApp(root)
    root.mainloop()
