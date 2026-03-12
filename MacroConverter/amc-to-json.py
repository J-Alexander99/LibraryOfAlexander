import xml.etree.ElementTree as ET
import json
import re
import os


# Key code mapping (common key codes)
KEY_CODE_MAP = {
    '225': 'Shift',
    '17': 'Ctrl',
    '18': 'Alt',
    '32': 'Space',
    '13': 'Enter',
    '27': 'Esc',
    '9': 'Tab',
    '69': 'E',
    '82': 'R',
    '81': 'Q',
    '87': 'W',
    '65': 'A',
    '83': 'S',
    '68': 'D',
    '70': 'F',
    '71': 'G',
    '72': 'H',
    '74': 'J',
    '75': 'K',
    '76': 'L',
    '90': 'Z',
    '88': 'X',
    '67': 'C',
    '86': 'V',
    '66': 'B',
    '78': 'N',
    '77': 'M',
}


def parse_amc_file(file_path):
    """Parse AMC XML file and extract macro commands."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find the KeyDown/Syntax section
    key_down = root.find('.//KeyDown/Syntax')
    if key_down is None or key_down.text is None:
        raise ValueError("No KeyDown/Syntax section found in AMC file")
    
    return key_down.text.strip()


def convert_amc_to_json(amc_commands):
    """Convert AMC macro commands to JSON format."""
    actions = []
    lines = amc_commands.split('\n')
    current_delay = 50  # Default delay
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Parse delay commands
        if line.startswith('Delay'):
            match = re.match(r'Delay\s+(\d+)\s*ms', line)
            if match:
                current_delay = int(match.group(1))
        
        # Parse mouse left button down
        elif line.startswith('LeftDown'):
            actions.append({
                "keyValue": "Mouse-Left",
                "keyValueType": 2,
                "type": 1,
                "delay": current_delay
            })
            current_delay = 50  # Reset to default after use
        
        # Parse mouse left button up
        elif line.startswith('LeftUp'):
            actions.append({
                "keyValue": "Mouse-Left",
                "keyValueType": 2,
                "type": 0,
                "delay": current_delay
            })
            current_delay = 50
        
        # Parse keyboard key down
        elif line.startswith('KeyDown'):
            match = re.match(r'KeyDown\s+(\d+)', line)
            if match:
                key_code = match.group(1)
                key_name = KEY_CODE_MAP.get(key_code, f"Key{key_code}")
                actions.append({
                    "keyValue": key_name,
                    "keyValueType": 1,
                    "type": 1,
                    "delay": current_delay
                })
                current_delay = 50
        
        # Parse keyboard key up
        elif line.startswith('KeyUp'):
            match = re.match(r'KeyUp\s+(\d+)', line)
            if match:
                key_code = match.group(1)
                key_name = KEY_CODE_MAP.get(key_code, f"Key{key_code}")
                actions.append({
                    "keyValue": key_name,
                    "keyValueType": 1,
                    "type": 0,
                    "delay": current_delay
                })
                current_delay = 50
    
    return {
        "mode": 2,
        "actions": actions
    }


def main():
    """Main conversion function."""
    amc_folder = "amc"
    json_folder = "json"
    
    # Ensure json folder exists
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    
    # Get all .amc files
    amc_files = [f for f in os.listdir(amc_folder) if f.endswith('.amc')]
    
    if not amc_files:
        print("No .amc files found in the amc folder.")
        return
    
    print("Available .amc files:")
    for i, file in enumerate(amc_files, 1):
        print(f"{i}. {file}")
    
    # Get user input
    choice = input("\nEnter the number of the file to convert (or 'all' for all files): ").strip()
    
    if choice.lower() == 'all':
        files_to_convert = amc_files
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(amc_files):
                files_to_convert = [amc_files[index]]
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Invalid input.")
            return
    
    # Convert files
    for amc_file in files_to_convert:
        try:
            amc_path = os.path.join(amc_folder, amc_file)
            json_filename = os.path.splitext(amc_file)[0] + '.json'
            json_path = os.path.join(json_folder, json_filename)
            
            print(f"\nConverting {amc_file}...")
            
            # Parse and convert
            amc_commands = parse_amc_file(amc_path)
            json_data = convert_amc_to_json(amc_commands)
            
            # Write to JSON file
            with open(json_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            print(f"✓ Successfully converted to {json_filename}")
            print(f"  {len(json_data['actions'])} actions generated")
            
        except Exception as e:
            print(f"✗ Error converting {amc_file}: {str(e)}")
    
    print("\nConversion complete!")


if __name__ == "__main__":
    main()
