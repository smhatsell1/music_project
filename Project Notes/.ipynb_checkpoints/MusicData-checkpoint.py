import numpy as np
import pandas as pd
import librosa
import requests
import subprocess
from colorsys import hsv_to_rgb
from manim import *

from original_preview_request import preview_request, convert_to_wav


#AUDIO FUNCTIONS
def extract_max_pitches(y, sr, beat_times, duration=0.1):
    pitches = []
    for time in beat_times:
        start_sample = int(time * sr)
        end_sample = int((time + duration) * sr)
        segment = y[start_sample:end_sample]

        pitches_segment, magnitudes = librosa.core.piptrack(y=segment, sr=sr)
        
        max_pitch = np.max(pitches_segment)
        if max_pitch > 0:
            pitches.append(max_pitch)
        else:
            pitches.append(0)
    
    return np.array(pitches)


def extract_notes(y, sr, beat_times, duration=0.1):
    note_map = {
        'C': 1 / 7,      
        'C♯': 1.5 / 7,  
        'D': 2 / 7,     
        'D♯': 2.5 / 7, 
        'E': 3 / 7,  
        'F': 4 / 7,     
        'F♯': 4.5 / 7,  
        'G': 5 / 7,     
        'G♯': 5.5 / 7,  
        'A': 6 / 7,    
        'A♯': 5.5 / 7,
        'B': 7 / 7      
    }

    pitches = extract_max_pitches(y, sr, beat_times)
    volumes = extract_max_volume(y, sr, beat_times)

    notes = librosa.hz_to_note(pitches, octave=False)
    numeric_notes = [note_map[note] if note in note_map else 0 for note in notes]
    return numeric_notes


def extract_max_volume(y, sr, beat_times, duration=0.1):
    volumes = []
    for time in beat_times:
        start_sample = int(time * sr)
        end_sample = int((time + duration) * sr)
        segment = y[start_sample:end_sample]

        rms = librosa.feature.rms(y=segment)
        rms_db = librosa.amplitude_to_db(rms)
        
        max_vol = np.max(rms_db)
        volumes.append(max_vol)
    
    return np.array(volumes)


###COLOR FUNCTIONS
def rgb_to_hex(rgb):
    '''
    param: tuple of rgb coded colors
    returns: hex string
    '''
    if type(rgb) != tuple:
        rgb = tuple(rgb)
    return '%02x%02x%02x' % rgb


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


#NORMALIZING FUNCTIONS
def norm_for_color(array):
    min_val = np.min(array)
    max_val = np.max(array)
    
    normalized_array = (array - min_val) / (max_val - min_val) * 255
    return normalized_array


def norm_to_n(array, n=1):
    '''
    param: np array
    returns: np array normalized between 0-n
    '''
    min_val = np.min(array)
    max_val = np.max(array)
    
    normalized_array = (array - min_val) / (max_val - min_val) * n
    return normalized_array


###FUNCTION FOR STREAMLINES
def direction(pos, note_vectors):
    x_pos, y_pos = pos[0], pos[1]

    # Find the closest note in time (based on x_pos)
    closest_note = min(note_vectors, key=lambda note: abs(note[0] - x_pos))  # Find closest beat time to 'x'
    
    note = closest_note[1]  # Note value for the closest beat time
    beat_time = closest_note[0]  # The corresponding beat time

    note = (note * 2) - 1

    # Calculate the direction for the streamlines based on both beat time and note value
    direction_x = (note * x_pos) * UP # Movement up-right
    direction_y = (beat_time * y_pos) * LEFT  # movement left

    # Return the resulting direction vector (combining the two components)
    return direction_x + direction_y


#RETURNS LIST OF COLORS
def get_colors(song_name):
        # audio_file_name = preview_request()
        # y, sr = librosa.load(audio_file_name)
        audio_file_name = "song.wav"
        y, sr = librosa.load(audio_file_name)
        
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
        return ['#'+color for color in list_of_colors]