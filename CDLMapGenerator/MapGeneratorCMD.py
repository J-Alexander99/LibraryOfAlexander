import random

def generate_cdl_map_set():
    # Define the map pool for each mode
    hardpoint_maps = ["Skyline", "Vault", "Hacienda", "Protocol", "Red Card"]
    snd_maps = ["Rewind", "Red Card", "Hacienda", "Protocol", "Dealership"]
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

# Generate and print a random map set
if __name__ == "__main__":
    map_set = generate_cdl_map_set()
    for idx, (mode, map_name) in enumerate(map_set, start=1):
        print(f"Map {idx}: {mode} on {map_name}")
