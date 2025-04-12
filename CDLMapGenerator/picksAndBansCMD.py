import random

def get_choice(options, prompt):
    """
    Display available options and get a valid choice from the user.
    """
    print("\nAvailable Options:")
    for i, option in enumerate(options, 1):
        print(f"{i}: {option}")
    
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def cdl_map_draft():
    # Get team names
    team_1 = input("Enter the name of Team 1: ").strip()
    team_2 = input("Enter the name of Team 2: ").strip()
    
    # Coin flip to decide Team A and Team B
    coin_flip = random.choice([team_1, team_2])
    if coin_flip == team_1:
        team_a = team_1
        team_b = team_2
    else:
        team_a = team_2
        team_b = team_1

    print(f"\nCoin flip result: {team_a} is Team A, {team_b} is Team B\n")

    # Map pools
    hardpoint_maps = ["Skyline", "Vault", "Hacienda", "Protocol", "Red Card"]
    snd_maps = ["Rewind", "Red Card", "Hacienda", "Protocol", "Dealership"]
    control_maps = ["Hacienda", "Protocol", "Vault"]

    # Map 1 and Map 4 (Hardpoint)
    available_hardpoint_maps = hardpoint_maps[:]
    print("**Hardpoint Map Picks**")
    team_a_ban = get_choice(available_hardpoint_maps, f"{team_a}, choose a map to ban: ")
    available_hardpoint_maps.remove(team_a_ban)
    print(f"{team_a} bans: {team_a_ban}")

    team_b_ban = get_choice(available_hardpoint_maps, f"{team_b}, choose a map to ban: ")
    available_hardpoint_maps.remove(team_b_ban)
    print(f"{team_b} bans: {team_b_ban}")

    map_1 = get_choice(available_hardpoint_maps, f"{team_a}, choose the map for Map 1 (Hardpoint): ")
    available_hardpoint_maps.remove(map_1)
    print(f"{team_a} picks Map 1: {map_1}")

    map_4 = get_choice(available_hardpoint_maps, f"{team_b}, choose the map for Map 4 (Hardpoint): ")
    available_hardpoint_maps.remove(map_4)
    print(f"{team_b} picks Map 4: {map_4}\n")

    # Map 2 and Map 5 (Search and Destroy)
    available_snd_maps = snd_maps[:]
    print("**Search and Destroy Map Picks**")
    team_b_ban = get_choice(available_snd_maps, f"{team_b}, choose a map to ban: ")
    available_snd_maps.remove(team_b_ban)
    print(f"{team_b} bans: {team_b_ban}")

    team_a_ban = get_choice(available_snd_maps, f"{team_a}, choose a map to ban: ")
    available_snd_maps.remove(team_a_ban)
    print(f"{team_a} bans: {team_a_ban}")

    map_2 = get_choice(available_snd_maps, f"{team_b}, choose the map for Map 2 (Search and Destroy): ")
    available_snd_maps.remove(map_2)
    print(f"{team_b} picks Map 2: {map_2}")

    map_5 = get_choice(available_snd_maps, f"{team_a}, choose the map for Map 5 (Search and Destroy): ")
    available_snd_maps.remove(map_5)
    print(f"{team_a} picks Map 5: {map_5}\n")

    # Map 3 (Control)
    available_control_maps = control_maps[:]
    print("**Control Map Pick**")
    team_a_ban = get_choice(available_control_maps, f"{team_a}, choose a map to ban: ")
    available_control_maps.remove(team_a_ban)
    print(f"{team_a} bans: {team_a_ban}")

    team_b_ban = get_choice(available_control_maps, f"{team_b}, choose a map to ban: ")
    available_control_maps.remove(team_b_ban)
    print(f"{team_b} bans: {team_b_ban}")

    map_3 = get_choice(available_control_maps, f"{team_a}, choose the map for Map 3 (Control): ")
    print(f"{team_a} picks Map 3: {map_3}\n")

    # Final Map Set
    print("**Final Map Set**")
    print(f"Map 1 (Hardpoint): {map_1}")
    print(f"Map 2 (Search and Destroy): {map_2}")
    print(f"Map 3 (Control): {map_3}")
    print(f"Map 4 (Hardpoint): {map_4}")
    print(f"Map 5 (Search and Destroy): {map_5}")

if __name__ == "__main__":
    cdl_map_draft()
