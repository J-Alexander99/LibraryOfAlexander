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


def find_items_in_spoiler(wanted_items, spoiler_filename="spoiler.txt"):
    """
    Search through the spoiler log for wanted items.
    Returns a dictionary with item names as keys and their location info as values.
    """
    found_items = {}
    
    try:
        with open(spoiler_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Search for each wanted item in the spoiler log
        for item in wanted_items:
            item_lower = item.lower()
            matching_lines = []
            
            for line in lines:
                # Only include lines where the item is FOUND, not REPLACED
                # Format: "[Item] in [Location]: ... Replaces [something]"
                # We want lines that start with the item name, not end with "Replaces [item]"
                if item_lower in line.lower():
                    # Check if this line shows where the item IS (not what replaced it)
                    # The item should appear at the start of the line before " in "
                    line_stripped = line.strip()
                    if line_stripped.lower().startswith(item_lower + " in"):
                        matching_lines.append(line_stripped)
            
            if matching_lines:
                found_items[item] = matching_lines
        
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
            for item, locations in found_items.items():
                f.write(f"\n{item}:\n")
                f.write("-" * 60 + "\n")
                for location in locations:
                    f.write(f"  {location}\n")
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
