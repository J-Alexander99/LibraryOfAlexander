import os
from tkinter import Tk, filedialog

def generate_tree(startpath):
    tree_lines = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = '    ' * level
        tree_lines.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = '    ' * (level + 1)
        for f in files:
            tree_lines.append(f"{sub_indent}{f}")
    return "\n".join(tree_lines)

def select_folder_and_generate_tree():
    # Hide the Tkinter root window
    root = Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory(title="Select a Folder")
    if folder_selected:
        tree_structure = generate_tree(folder_selected)
        print("Folder Tree:")
        print(tree_structure)
        
        # Save to clipboard
        root.clipboard_clear()
        root.clipboard_append(tree_structure)
        root.update()  # Now it stays in clipboard after program closes
        print("\nTree structure copied to clipboard!")
    else:
        print("No folder selected.")

if __name__ == "__main__":
    select_folder_and_generate_tree()
