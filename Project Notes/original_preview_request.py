import os
import requests
import subprocess


def preview_request(): 
    """Prompts the user for a song title, searches for it on Deezer's API, 
    retrieves a 30-second preview of the song, and saves it as an MP3 file in folder 'songs'. 
    Then converts the MP3 preview to a WAV file and returns the path to the WAV file.
    params: NONE
    returns: path to the WAV file.
    """
    base_url = "https://api.deezer.com/search"

    query = input("Enter a song title: ")  # Prompt user for input if no query is provided

    print(f"Searching for: {query}")
    
    search = requests.get(f"{base_url}?q={query}")

    # Check for valid response
    if search.status_code == 200:
        data = search.json()

        #Check if search data is empty
        if data['data']:
            track = data['data'][0] # First song in the search
            
            preview_url = track['preview'] # Get preview url
            title = track['title']
            artist = track['artist']['name']
            
            preview_response = requests.get(preview_url) # Retrieve preview from url

            # Check if preview URL was retrieved successfully
            if preview_response.status_code == 200:
                if not os.path.exists('songs'):
                    os.makedirs('songs')
                # Save the preview as an MP3 file
                song_preview_file = f"songs/{title}_{artist}_preview.mp3"
                with open(song_preview_file, 'wb') as f:
                    f.write(preview_response.content)
                wav_file = f"songs/{title}_{artist}_preview.wav"
                convert_to_wav(song_preview_file, wav_file)

                return wav_file
                print(f"The 30-second preview has been saved as {title}_{artist}_preview.wav.")
            else:
                print(f"Failed to download the preview audio. Status Code: {preview_response.status_code}.")
    else:
        print(f"Failed to search. Status Code: {search.status_code}")



def convert_to_wav(input_file, output_file):
    """Converts an audio file from MP3 format to WAV format using ffmpeg.
    
    Args:
        input_file (str): Path to the input MP3 file.
        output_file (str): Path to save the converted WAV file.
    """
    command = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(command)

    

#Runs only in the command line
if __name__ == "__main__":
    preview_request()
