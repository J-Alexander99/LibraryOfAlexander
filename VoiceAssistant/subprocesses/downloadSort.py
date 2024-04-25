import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import shutil

def recognize_speech():
    # Function to recognize speech using Google's Speech Recognition
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None

def speaksound(text):
    # Function to use gTTS to speak the given text
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    play(AudioSegment.from_file("temp.mp3"))  # Use pydub's play function
    os.remove("temp.mp3")

def create_sorted_folders(sorted_folder):
    # Function to create 'code', 'media', 'games', and 'other' folders within 'sorted'
    folders = ['code', 'media', 'games', 'other']
    for folder_name in folders:
        folder_path = os.path.join(sorted_folder, folder_name)
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

def sort_downloads(sorted_folder):
    # Function to sort files in the downloads folder into user-specified folders
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    files = [f for f in os.listdir(downloads_folder) if os.path.isfile(os.path.join(downloads_folder, f))]
    
    for file in files:
        file_path = os.path.join(downloads_folder, file)
        
        # Read out the name of the file
        speaksound(f"Now sorting file {file}")
        
        print(f"Move {file} to which folder? Options are:")
        
        # Dynamically get the list of folders in the sorted folder
        destination_options = get_folder_list(sorted_folder)
        
        # Print the available options
        print("\n".join(destination_options))
        
        destination = recognize_speech()
        
        if destination and destination in destination_options:
            destination_path = os.path.join(sorted_folder, destination)
            
            # Ensure the destination folder exists; create if not
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            
            # Move the file to the destination folder
            os.rename(file_path, os.path.join(destination_path, file))
            print(f"Moved {file} to {destination_path}")
    
    # Announce that the downloads folder is sorted
    speaksound("Downloads folder is now sorted.")

def get_folder_list(folder_path):
    # Function to get a list of folders in a specified path
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    return folders

def move_sorted_folder_to_storage(sorted_folder, storage_folder):
    # Function to move the sorted folder to the specified storage folder
    shutil.move(sorted_folder, storage_folder)
    print(f"Moved sorted folder to {storage_folder}")

def main():
    # Check if the "sorted" folder exists on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    sorted_folder = os.path.join(desktop_path, "sorted")

    if not os.path.exists(sorted_folder):
        # Create "sorted" folder and subfolders if it doesn't exist
        os.makedirs(sorted_folder)
        print(f"Created folder: {sorted_folder}")
        create_sorted_folders(sorted_folder)

    # Main loop for continuous sorting
    while True:
        sort_downloads(sorted_folder)
        
        # Prompt the user to move the sorted folder to storage using text-to-speech
        speaksound("Do you want to move the sorted folder to storage? Please say yes or no.")
        response = recognize_speech()
        if response and response.lower() == 'yes':
            # Specify the path to the storage folder
            storage_folder = "/path/to/storage"
            move_sorted_folder_to_storage(sorted_folder, storage_folder)
            break  # End the program after moving the sorted folder


if __name__ == "__main__":
    main()
