import sys
import yt_dlp as youtube_dl
from datetime import datetime
import json
import os

def get_last_videos_info(channel_url, num_videos=10):
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',
        'playlistend': num_videos  # Fetch the last `num_videos` videos
    }

    videos = []

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(channel_url, download=False)
            if 'entries' in info_dict:
                for video in info_dict['entries']:
                    video_title = video['title']
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                    
                    # Fetch detailed info for the video to get the upload date
                    detailed_info = ydl.extract_info(video_url, download=False)
                    upload_date = detailed_info.get('upload_date')
                    
                    if upload_date:
                        upload_date = datetime.strptime(upload_date, "%Y%m%d").strftime("%d/%m/%Y")
                    else:
                        upload_date = "Unknown"
                    
                    # Add watched attribute with default value False
                    videos.append({
                        'title': video_title,
                        'url': video_url,
                        'upload_date': upload_date,
                        'watched': False  # Default value
                    })
            
            return videos
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

def save_to_json(videos, output_file):
    # Check if the file already exists
    if os.path.exists(output_file):
        # Load existing data from the file
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    # Update existing videos with new ones and set watched to False by default
    updated_data = existing_data.copy()
    for video in videos:
        if not any(v['url'] == video['url'] for v in existing_data):
            updated_data.append(video)

    # Write all data back to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Ensure a channel URL is provided as command-line argument
    if len(sys.argv) < 2:
        print("Usage: python fetch_youtube_videos.py <channel_url>")
        sys.exit(1)
    
    channel_url = sys.argv[1]
    json_file = os.path.join(os.path.dirname(__file__), 'videos.json')
    num_videos = 10
    videos = get_last_videos_info(channel_url, num_videos)
    
    if videos:
        # Save to JSON file
        save_to_json(videos, json_file)
        print(f"Added {len(videos)} new videos to {json_file}")
    else:
        print("No videos found.")
