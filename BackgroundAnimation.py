import numpy as np
import pandas as pd
import librosa
import requests
import subprocess
from manim import *

#run: manim -pql BackgroundAnimation.py colorChanger

def preview_request():
    '''
    Gets song
    '''
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

    return query

def convert_to_wav(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(command)

def rgb_to_hex(rgb):
    '''
    param: tuple of rgb coded colors
    returns: hex string
    '''
    if type(rgb) != tuple:
        rgb = tuple(rgb)
    return '%02x%02x%02x' % rgb

def norm_for_color(array):
    min_val = np.min(array)
    max_val = np.max(array)
    
    normalized_array = (array - min_val) / (max_val - min_val) * 255
    return normalized_array



class colorChanger(Scene):
    def construct(self):
        audio_file_name = preview_request()
        y, sr = librosa.load(audio_file_name)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        song_time = librosa.get_duration(y=y, sr=sr)
        percent_through_song = beat_times/song_time


        num_to_take_from_y_1 = (percent_through_song*y.size).astype(int)
        num_to_take_from_y_2 = ((percent_through_song-0.01)*y.size).astype(int)
        num_to_take_from_y_3 = ((percent_through_song+0.01)*y.size).astype(int)

        # Normalize the audio values to generate RGB color channels
        r = norm_for_color(y[num_to_take_from_y_1]).astype(int)
        b = norm_for_color(y[num_to_take_from_y_2]).astype(int)
        g = norm_for_color(y[num_to_take_from_y_3]).astype(int)

        zip_obj = zip(r,b,g)
        color_list = list(zip_obj)

        vectorized_function = np.vectorize(rgb_to_hex, signature='(n)->()')
        list_of_colors = vectorized_function(np.array(color_list))

        cues = np.diff(beat_times)
        
        self.add_sound(audio_file_name)

        for i in range(len(cues)):
            self.wait(cues[i])
            self.camera.background_color = "#"+list_of_colors[i]
        









