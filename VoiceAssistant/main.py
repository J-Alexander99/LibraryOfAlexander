import os
import subprocess
import speech_recognition as sr
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def list_files(folder_path):
    """List files in the specified folder."""
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return files

def run_file(file_path, parameter=None):
    """Run the specified file using subprocess."""
    command = ['python', file_path]

    if parameter is not None:
        command.extend(parameter.split())

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(f"Successfully executed: {file_path}")
        print(f"Output:\n{result.stdout}")
        print(f"Errors (if any):\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {file_path}: {e}")
        print(f"Error output:\n{e.stdout}")
        print(f"Error details:\n{e.stderr}")

def voice_command():
    """Listen for a voice command."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower().strip()
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the command.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def voice_input():
    """Listen for voice input."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something for the parameter...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        result = recognizer.recognize_google(audio, show_all=True)
        print(f"Debug: Full recognition result: {result}")

        if 'alternative' in result and result['alternative'][0]['confidence'] > 0.7:
            # Extract the first alternative (most likely recognized)
            parameter = result['alternative'][0]['transcript'].strip()
            print(f"Debug: Recognized parameter: {parameter}")
            return parameter
        else:
            print("Error: No alternative recognized or confidence below threshold.")
            return None
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the parameter.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None



def main():
    # Specify the folder containing the files you want to run
    folder_path = 'C:/Users/joela/Desktop/ClarityAI/subprocesses'

    # List files in the specified folder
    files = list_files(folder_path)

    if not files:
        print(f"No files found in {folder_path}")
        return

    # Display the list of files
    print("Files in the folder:")
    for idx, file_name in enumerate(files, start=1):
        print(f"{idx}. {file_name}")

    # Create a dictionary mapping lowercased file names to execute commands
    command_mapping = {file_name.lower(): f"execute {file_name.lower()}" for file_name in files}

    # Allow users to define custom voice commands with parameters
    custom_commands = {
        "custom1": "execute custom_script1.py",
        "custom2": "execute custom_script2.py",
        "youtube player": "execute youtubeVideoPlayer.py {param}",
        # Add more custom commands as needed
    }

    # Merge custom commands into the command mapping
    command_mapping.update({k.lower(): v for k, v in custom_commands.items()})

    # Wait for a voice command
    command = voice_command()

    if not command:
        return

    print(f"Debug: Command after voice_command: {command}")

    # Check if the lowercased command closely matches a file or custom command
    lowercased_command = command.lower()
    print(f"Debug: Lowercased command: {lowercased_command}")

    matching_commands = max(command_mapping, key=lambda c: similarity(lowercased_command, c.lower()))

    match_ratio = similarity(lowercased_command, matching_commands.lower())
    if match_ratio > 0.7:  # Adjust the threshold as needed
        selected_command = command_mapping[matching_commands]
        print(f"Debug: Selected command: {selected_command}")

        # Extract parameters if the command contains {param}
        if "{param}" in selected_command:
            # Get the parameter from voice input
            parameter = voice_input()
            if parameter is not None:
                parameter = parameter.replace(" ", "-")  # TEST CODE REMOVE LATER-----------------------------------------------------
                selected_command = selected_command.replace("{param}", parameter)
                print(f"Debug: Updated command with parameter: {selected_command}")
        else:
            # If the command doesn't require a parameter, set it to an empty string or None
            parameter = None

    # Run the selected file or custom command
    if selected_command.startswith("execute "):
        # Extract the file_name from the selected command
        file_name = selected_command.split(" ")[1]

        # Build the full file path
        file_path = os.path.join(folder_path, file_name)

        # Print the recognized parameter (if any)
        print(f"Debug: Recognized parameter: {parameter}")

        # Replace the {param} placeholder with the actual parameter
        selected_command = selected_command.replace("{param}", str(parameter))

        # Print debug information
        print(f"Debug: Selected command: {selected_command}")
        print(f"Debug: File path: {file_path}")

        # Run the file with the updated command and parameter
        run_file(file_path, parameter)

if __name__ == "__main__":
    main()
