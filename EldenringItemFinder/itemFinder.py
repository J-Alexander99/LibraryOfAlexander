"""
Elden Ring Randomizer Item Finder
Searches through randomizer spoiler logs to find specific items you're looking for.
"""

def read_wanted_items(filename="wanted_items.txt"):
    """Read the list of items to search for."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Read lines, strip whitespace, and filter out empty lines
            items = [line.strip() for line in f.readlines() if line.strip()]
        return items
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []


def extract_enemy_info(line):
    """Extract enemy name and ID from a spoiler line if it's dropped by an enemy."""
    import re
    
    # Look for patterns like "Dropped by [Enemy]" or "From [Enemy]"
    # Enemy names may include IDs like (#12345)
    pattern = r'(?:Dropped by|From)\s+(.+?)(?:\s*\(#(\d+)\))?\.'
    match = re.search(pattern, line)
    
    if match:
        enemy_name = match.group(1).strip()
        enemy_id = match.group(2) if match.group(2) else None
        
        # Exclude common non-enemy sources
        excluded = ['chest', 'corpse', 'smouldering corpse', 'robed corpse', 
                   'lidded river chest', 'giant ball']
        if enemy_name.lower() not in excluded:
            return enemy_name, enemy_id
    
    return None, None


def build_enemy_lookup(spoiler_lines):
    """Build a dictionary of enemy replacements for fast lookup."""
    import re
    enemy_replacements = {}
    
    # Find all "Replacing" lines in the spoiler log
    for line in spoiler_lines:
        if 'replacing' in line.lower():
            # Format: "Replacing [Original Enemy] (#ID) in [Location]: [New Enemy] (#ID2) from [Location2]"
            match = re.search(r'Replacing\s+(.+?)\s+\(#(\d+)\).+?:\s+(.+?)\s+\(#\d+\)', line, re.IGNORECASE)
            if match:
                original_enemy = match.group(1).strip()
                enemy_id = match.group(2).strip()
                new_enemy = match.group(3).strip()
                
                # Store by both name and ID
                enemy_replacements[original_enemy.lower()] = new_enemy
                enemy_replacements[enemy_id] = new_enemy
    
    return enemy_replacements


def find_items_in_spoiler(wanted_items, spoiler_filename="spoiler.txt"):
    """
    Search through the spoiler log for wanted items.
    Returns a dictionary with item names as keys and their location info as values.
    """
    found_items = {}
    
    try:
        with open(spoiler_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Build enemy lookup table once for performance
        enemy_replacements = build_enemy_lookup(lines)
        
        # Search for each wanted item in the spoiler log
        for item in wanted_items:
            item_lower = item.lower()
            matching_entries = []
            
            for line in lines:
                # Only include lines where the item is FOUND, not REPLACED
                line_stripped = line.strip()
                if line_stripped.lower().startswith(item_lower + " in"):
                    # Check if it's from an enemy
                    enemy_name, enemy_id = extract_enemy_info(line_stripped)
                    enemy_info = None
                    
                    if enemy_name:
                        # Look up what the enemy has been randomized into
                        new_enemy = None
                        if enemy_id and enemy_id in enemy_replacements:
                            new_enemy = enemy_replacements[enemy_id]
                        elif enemy_name.lower() in enemy_replacements:
                            new_enemy = enemy_replacements[enemy_name.lower()]
                        
                        if new_enemy:
                            enemy_info = f"    → Enemy: {enemy_name} is now: {new_enemy}"
                    
                    matching_entries.append({
                        'location': line_stripped,
                        'enemy_info': enemy_info
                    })
            
            if matching_entries:
                found_items[item] = matching_entries
        
        return found_items
    
    except FileNotFoundError:
        print(f"Error: {spoiler_filename} not found!")
        return {}


def write_results(found_items, output_filename="results.txt"):
    """Write the found items and their locations to a results file."""
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            if not found_items:
                f.write("No items found!\n")
                print("No items found in the spoiler log.")
                return
            
            # Write header
            f.write("=" * 60 + "\n")
            f.write("ELDEN RING RANDOMIZER - ITEM LOCATIONS\n")
            f.write("=" * 60 + "\n\n")
            
            # Write each found item and its locations
            for item, entries in found_items.items():
                f.write(f"\n{item}:\n")
                f.write("-" * 60 + "\n")
                for entry in entries:
                    f.write(f"  {entry['location']}\n")
                    if entry['enemy_info']:
                        f.write(f"{entry['enemy_info']}\n")
                f.write("\n")
            
            f.write("=" * 60 + "\n")
            f.write(f"Total items found: {len(found_items)}\n")
        
        print(f"Results written to {output_filename}")
        print(f"Found {len(found_items)} items")
        
    except Exception as e:
        print(f"Error writing results: {e}")


def main():
    """Main function to run the item finder."""
    print("=" * 60)
    print("Elden Ring Randomizer Item Finder")
    print("=" * 60)
    
    # Read the list of wanted items
    print("\nReading wanted items...")
    wanted_items = read_wanted_items()
    
    if not wanted_items:
        print("No items to search for. Add items to 'wanted_items.txt'")
        return
    
    print(f"Searching for {len(wanted_items)} items:")
    for item in wanted_items:
        print(f"  - {item}")
    
    # Search for items in the spoiler log
    print("\nSearching spoiler log...")
    found_items = find_items_in_spoiler(wanted_items)
    
    # Write results
    print("\nWriting results...")
    write_results(found_items)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
