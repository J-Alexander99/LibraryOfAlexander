import os
from tkinter import Tk, filedialog
import pyperclip  # Cross-platform clipboard library

def generate_tree(startpath):
    # Initialize a list to hold the tree lines
    tree_lines = []
    
    # Walk through the directory structure
    for root, dirs, files in os.walk(startpath):
        # Determine the current level in the directory tree
        level = root.replace(startpath, '').count(os.sep)
        # Create indentation based on the level
        indent = '    ' * level
        # Add the current directory to the tree with a trailing slash
        tree_lines.append(f"{indent}{os.path.basename(root)}/")
        
        # Create additional indentation for files in the directory
        sub_indent = '    ' * (level + 1)
        # Add each file to the tree
        for f in files:
            tree_lines.append(f"{sub_indent}{f}")
    
    # Join all lines with newline characters to create the final tree structure
    return "\n".join(tree_lines)

def select_folder_and_generate_tree():
    # Initialize the Tkinter root window but hide it
    root = Tk()
    root.withdraw()

    # Open a dialog for the user to select a folder
    folder_selected = filedialog.askdirectory(title="Select a Folder")
    if folder_selected:
        # Generate the folder tree structure
        tree_structure = generate_tree(folder_selected)
        print("Folder Tree:")
        print(tree_structure)
        
        try:
            # Use pyperclip for clipboard operations
            pyperclip.copy(tree_structure)
            clipboard_content = pyperclip.paste()  # Retrieve clipboard content
            
            if clipboard_content == tree_structure:
                print("\nTree structure successfully copied to clipboard!")
            else:
                raise ValueError("Clipboard content mismatch.")
        except Exception as e:
            # Handle clipboard errors gracefully
            print(f"\nFailed to copy to clipboard: {e}")
            # Fallback: Save to a file
            fallback_path = os.path.join(folder_selected, "folder_tree.txt")
            with open(fallback_path, "w") as file:
                file.write(tree_structure)
            print(f"Tree structure saved to {fallback_path}.")
    else:
        # Handle the case where no folder was selected
        print("No folder selected.")

# Run the function when the script is executed directly
if __name__ == "__main__":
    select_folder_and_generate_tree()
