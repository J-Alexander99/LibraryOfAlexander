import subprocess
import time
import os

def open_shortcut(shortcut_path):
    subprocess.Popen(['start', '', shortcut_path], shell=True)

if __name__ == "__main__":
    shortcuts_folder = "C:\\Users\\joela\\Desktop\\ClarityAI\\Assets\\shortcuts"

    elden_ring_shortcut = "er.lnk"
    ds4_windows_shortcut = "ds4.lnk"
    cheat_engine_shortcut = "ch.lnk"

    elden_ring_path = os.path.join(shortcuts_folder, elden_ring_shortcut)
    ds4_windows_path = os.path.join(shortcuts_folder, ds4_windows_shortcut)
    cheat_engine_path = os.path.join(shortcuts_folder, cheat_engine_shortcut)

    open_shortcut(elden_ring_path)
    time.sleep(2)  # Add a delay if needed between shortcut launches
    open_shortcut(ds4_windows_path)
    time.sleep(2)  # Add a delay if needed between shortcut launches
    open_shortcut(cheat_engine_path)
