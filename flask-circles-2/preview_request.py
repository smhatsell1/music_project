import requests
import os

# Function to download the song preview (30 seconds) from Deezer API
def preview_request(song_name=None): 
    """Searches for a song by title and downloads a 30-second preview as an MP3 file.

    If no song title is provided, prompts the user to enter one. The function fetches 
    track data from the Deezer API, retrieves the preview URL, and saves the audio 
    preview to a local file in the 'static/songs' directory.

    Parameters:
    song_name (str): The title of the song to search for. If None, the user will be prompted for input.

    Returns: MIGHT CHANGE!!!!!!!
    str: The path to the saved MP3 preview file.
    """
    base_url = "https://api.deezer.com/search"

    # Prompt user for input if no query is provided
    if song_name == None:
        query = input("Enter a song title: ")
    else: #else use input
        query = song_name

    print(f"Searching for: {query}")

    #Make API request
    search = requests.get(f"{base_url}?q={query}")

    # Check for valid response
    if search.status_code == 200:
        data = search.json()

        #Check if data is empty
        if data['data']:
            # Get first song in the search
            track = data['data'][0]

            preview_url = track['preview'] #Get preview url
            title = track['title'] #Get title
            artist = track['artist']['name'] #get artist name

            preview_response = requests.get(preview_url)

            if preview_response.status_code == 200:
                if not os.path.exists('static/songs'):
                    os.makedirs('static/songs')
                # Save the preview as an MP3 file
                output_file = f"static/songs/{title}_{artist}_preview.mp3"
                with open(output_file, 'wb') as f:
                    f.write(preview_response.content)

                print(f"The 30-second preview has been saved as {title}_{artist}_preview.mp3 in static/songs.")
            else:
                print("Failed to download the preview audio.")
    else:
        print(f"Failed to fetch track info. Status Code: {response.status_code}")

    return output_file


# #Runs in the command line
# if __name__ == "__main__":
#     preview_request()