
import sys
from youtubesearchpython import VideosSearch
import webbrowser

def play_first_video_on_youtube(search_query):
    # Perform the YouTube search
    videos_search = VideosSearch(search_query, limit=1)
    results = videos_search.result()

    # Check if there are any search results
    if len(results['result']) > 0:
        # Extract the URL of the first video
        video_url = results['result'][0]['link']

        # Open the video URL in the default web browser
        webbrowser.open(video_url)
        print(f"Opening the first video on YouTube for '{search_query}'...")
    else:
        print(f"No videos found on YouTube for '{search_query}'.")

if __name__ == "__main__":
    # Check if the script is provided with a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python youtubeVideoPlayer.py <search_query>")
        sys.exit(1)

    # Get the search word from the command-line argument
    search_word = sys.argv[1]

    # Call the function to play the first video on YouTube for the given word
    play_first_video_on_youtube(search_word)
