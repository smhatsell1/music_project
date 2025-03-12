import numpy as np
import pandas as pd

import librosa
from manim import *
from colorsys import hsv_to_rgb
import os

#run: manim -pql HSV_Anim.py hsvAnim
#or
#run: manim render -pql --flush_cache HSV_Anim.py hsvAnim


#Normalize to a 0-n rnage
def norm_to_n(array, n=1):
    '''
    param: np array
    returns: np array normalized between 0-n
    '''
    min_val = np.min(array)
    max_val = np.max(array)
    
    normalized_array = (array - min_val) / (max_val - min_val) * n
    return normalized_array


# Function to extract pitch at specific timestamps
def extract_max_pitches(y, sr, beat_times, duration=0.1):
    pitches = []
    for time in beat_times:
        # Extract a segment of audio around each timestamp
        start_sample = int(time * sr)
        end_sample = int((time + duration) * sr)
        segment = y[start_sample:end_sample]

        # Get pitch
        pitches_segment, magnitudes = librosa.core.piptrack(y=segment, sr=sr)
        
        # Get the maximum pitch from the frame with the highest magnitude
        max_pitch = np.max(pitches_segment)
        if max_pitch > 0:
            pitches.append(max_pitch)
        else:
            pitches.append(0)
    
    return np.array(pitches)


def extract_max_volume(y, sr, beat_times, duration=0.1):
    volumes = []
    for time in beat_times:
        # Extract a segment of audio around each timestamp
        start_sample = int(time * sr)
        end_sample = int((time + duration) * sr)
        segment = y[start_sample:end_sample]

        # Get volume
        rms = librosa.feature.rms(y=segment)
        rms_db = librosa.amplitude_to_db(rms)
        
        # Get the maximum volume
        max_vol = np.max(rms_db)
        volumes.append(max_vol)
    
    return np.array(volumes)


def hsv_to_hex(hsv):
    h, s, v = hsv
    #Convert 
    h = h/360
    s = s/100
    v = v/100
    
    r, g, b = hsv_to_rgb(h, s, v)
    
    # Convert RGB to HEX
    hex_color = '{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
    
    return hex_color


class hsvAnim(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Retrieve song_path from the environment variable
        self.song_path = os.getenv("SONG_PATH")
            
    def construct(self):
        y, sr = librosa.load(self.song_path)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        song_time = librosa.get_duration(y=y, sr=sr)

        note_map = {
            'C':1,'C♯':1.5,
            'D':2,'D♯':2.5,
            'E':3,
            'F':4,'F♯':4.5,
            'G':5,'G♯':5.5,
            'A':6,'A♯':5.5,
            'B':7
        }

        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        norm_centroid = (spectral_centroid - spectral_centroid.min()) / (spectral_centroid.max() - spectral_centroid.min())

        pitches = extract_max_pitches(y, sr, beat_times)
        volumes = extract_max_volume(y, sr, beat_times)

        notes = librosa.hz_to_note(pitches, octave=False)
        note_vals = [note_map[note] for note in notes]

        H = norm_to_n(note_vals,360)
        S = norm_to_n(volumes, 100)
        B = norm_to_n(pitches, 100)


        zip_obj = zip(H,S,B)
        color_list = list(zip_obj)

        vectorized_function = np.vectorize(hsv_to_hex, signature='(n)->()')
        list_of_colors = vectorized_function(np.array(color_list))

        cues = np.diff(beat_times)
        
        self.add_sound(self.song_path)


        for i in range(len(cues)):
            text = Text(f"{beat_times[i]:.2f}", font_size=144)
            # text size expands during high frequency sounds 
            text.scale(1 + norm_centroid[i] * 6)
            
            self.add(text)  
            self.wait(cues[i])
            self.camera.background_color = "#"+list_of_colors[i]
            self.remove(text)
            
        self.wait(3)
        









