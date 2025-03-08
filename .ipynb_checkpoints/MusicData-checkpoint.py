import numpy as np
import pandas as pd
import librosa
import requests
import subprocess
from manim import *

from preview_request import preview_request, convert_to_wav



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
            pitches.append(0)  # No pitch detected
    
    return np.array(pitches)

def extract_notes(y, sr, beat_times, duration=0.1):
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
    numeric_notes = [note_map[note] if note in note_map else 0 for note in notes]
    return numeric_notes

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
