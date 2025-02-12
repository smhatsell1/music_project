import requests


base_url = "https://api.deezer.com/search"


query = "Shape of You" #Developer Note: Set to change

search = requests.get(f"{base_url}?q={query}")

# Check for valid response
if search.status_code == 200:
    data = search.json()

    #Check if data is empty
    if data['data']:
        track = data['data'][0] # First song in the search

        preview_url = track['preview'] #Get preview url
        preview_response = requests.get(preview_url)
        # Check if preview URL was retrieved successfully
        if preview_response.status_code == 200:
            # Save the preview as an MP3 file
            output_file = f"{query}_preview.mp3"
            with open(output_file, 'wb') as f:
                f.write(preview_response.content)
            print(f"The 30-second preview has been saved as {output_file}.")
        else:
            print("Failed to download the preview audio.")
else:
    print(f"Failed to fetch track info. Status Code: {response.status_code}")
