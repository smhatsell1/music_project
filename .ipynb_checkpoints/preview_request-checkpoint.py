import requests
import subprocess


def preview_request(): 
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
                # Save the preview as an MP3 file
                song_preview_file = f"{title}_{artist}_preview.mp3" # Maybe change to be the name of the song title, artist?
                with open(song_preview_file, 'wb') as f:
                    f.write(preview_response.content)
                wav_file = f"{title}_{artist}_preview.wav"
                convert_to_wav(song_preview_file, wav_file)

                return wav_file
                print(f"The 30-second preview has been saved as {title}_{artist}_preview.wav.")
            else:
                print(f"Failed to download the preview audio. Status Code: {preview_response.status_code}.")
    else:
        print(f"Failed to search. Status Code: {search.status_code}")



def convert_to_wav(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(command)

    

#Runs only in the command line
if __name__ == "__main__":
    preview_request()
