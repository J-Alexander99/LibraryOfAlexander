import tkinter as tk
import json
import webbrowser

def mark_as_watched(video_url):
    # Update the watched status in the JSON file
    with open('videos.json', 'r+', encoding='utf-8') as f:
        videos = json.load(f)
        for video in videos:
            if video['url'] == video_url:
                video['watched'] = True
                break
        f.seek(0)  # Move cursor to the beginning of the file
        json.dump(videos, f, indent=4)
        f.truncate()  # Truncate remaining content (in case new content is shorter)
    
    # Refresh the display after marking as watched
    refresh_display()

def refresh_display():
    # Read videos from JSON file
    with open('videos.json', 'r', encoding='utf-8') as f:
        videos = json.load(f)
    
    # Clear previous content
    for widget in video_frame.winfo_children():
        widget.destroy()
    
    # Display videos in a scrollable Text widget
    text = tk.Text(video_frame, wrap='word')
    text.pack(side='left', fill='both', expand=True)
    
    # Scrollbar for the text widget
    scrollbar = tk.Scrollbar(video_frame, orient='vertical', command=text.yview)
    scrollbar.pack(side='right', fill='y')
    
    text.config(yscrollcommand=scrollbar.set)
    
    for video in videos:
        if not video['watched']:
            title = video['title']
            url = video['url']
            
            # Format the display
            display_text = f"{title}\n\n"
            
            # Add clickable link
            text.tag_configure(url, foreground='blue', underline=True)
            text.insert('end', display_text, url)
            text.tag_bind(url, '<Button-1>', lambda event, url=url: webbrowser.open_new(url))
            
            # Add button to mark as watched
            mark_button = tk.Button(text, text="Mark as Watched", command=lambda url=url: mark_as_watched(url))
            text.window_create('end', window=mark_button)
            text.insert('end', '\n\n')
    
    text.configure(state='disabled')  # Make the text widget read-only

# Create Tkinter window
root = tk.Tk()
root.title("YouTube Videos Tracker")

# Frame for videos display
video_frame = tk.Frame(root)
video_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Refresh button
refresh_button = tk.Button(root, text="Refresh", command=refresh_display)
refresh_button.pack(pady=10)

# Initial display
refresh_display()

# Start the Tkinter main loop
root.mainloop()
