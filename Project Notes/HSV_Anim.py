import numpy as np
import pandas as pd
import librosa
import requests
import subprocess
from manim import *
from colorsys import hsv_to_rgb

from original_preview_request import preview_request, convert_to_wav
from MusicData.py import *


#run: manim -pql HSV_Anim.py hsvAnim

class hsvAnim(Scene):
    def construct(self):
        audio_file_name = preview_request()
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

        cues = np.diff(beat_times)
        
        self.add_sound(audio_file_name)


        for i in range(len(cues)):
            text = Text(f"{cues[i]}", font_size=144)
            self.add(text)  
            self.wait(cues[i])

            self.camera.background_color = "#"+list_of_colors[i]
            self.remove(text)
        









