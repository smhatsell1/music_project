#LIBRARIES
import numpy as np
import pandas as pd
import librosa
import requests
import subprocess
from manim import *

#import other code we've written
from original_preview_request import preview_request, convert_to_wav
from MusicData import *

'''
To run either of these animations run one the following:
manim -pql BackgroundAnimation.py colorChanger
manim -pql BackgroundAnimation.py ContinuousMotion

ISSUES: 
- Last 3 seconds of animation is constant color
- Interpolation to fix janky movements

GOALS:
Speed:
    tempo
Colors:
    harmonic/percussive? 
    more harmonic = more blue more percussive = more red? Or volumes
Shape:
    vector field with notes over time, using note map, number of stream lines
'''

class colorChanger(Scene):
    """
    A Manim scene that changes the background color of the camera based on 
    the beat of a song. The song is analyzed to generate a color sequence 
    creating a dynamic background color effect synced with the song's tempo 
    and beat timings.
    **Actual colors do not (yet) reflect any information about the song**
    """
    def construct(self):
        audio_file_name = preview_request()
        y, sr = librosa.load(audio_file_name)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        song_time = librosa.get_duration(y=y, sr=sr)
        percent_through_song = beat_times/song_time


        num_to_take_from_y_1 = ((percent_through_song-0.02)*y.size).astype(int)
        num_to_take_from_y_2 = ((percent_through_song-0.01)*y.size).astype(int)
        num_to_take_from_y_3 = ((percent_through_song+0.00)*y.size).astype(int)

        # Normalize the audio values to generate RGB color channels
        r = norm_for_color(y[num_to_take_from_y_1]).astype(int)
        b = norm_for_color(y[num_to_take_from_y_2]).astype(int)
        g = norm_for_color(y[num_to_take_from_y_3]).astype(int)

        zip_obj = zip(r,b,g)
        color_list = list(zip_obj)

        vectorized_function = np.vectorize(rgb_to_hex, signature='(n)->()')
        color_sequence = vectorized_function(np.array(color_list))

        cues = np.diff(beat_times)
        
        self.add_sound(audio_file_name)
 
        for i in range(len(cues)):
            self.wait(cues[i])
            self.camera.background_color = "#"+color_sequence[i]

class ContinuousMotion(Scene):
    """
    A scene that extracts note information from the audio, calculates tempo 
    and beat timings, and uses the StreamLines 
    class to animate movement based on these notes. 
    
    The motion speed is determined by the tempo of the song.
    """
    def construct(self):
        audio_file_name = preview_request()
        y, sr = librosa.load(audio_file_name)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        song_time = librosa.get_duration(y=y, sr=sr)
        
        notes = extract_notes(y, sr, beat_times)
        note_vectors = list(zip(beat_times, notes))

        speed_factor= tempo/40 

        stream_lines = StreamLines(lambda pos: direction(pos, note_vectors), stroke_width=3, max_anchors_per_line=40,
            virtual_time=song_time,
            three_dimensions=False,
            padding=4)
        self.add(stream_lines)
        self.add_sound(audio_file_name)
        stream_lines.start_animation(warm_up=False, flow_speed=speed_factor)
        self.wait(30)

