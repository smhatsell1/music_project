import numpy as np
import pandas as pd
import librosa
import requests
import subprocess
from manim import *

from preview_request import preview_request, convert_to_wav
from MusicData import *

#run: manim -pql BackgroundAnimation.py colorChanger

#issue: last 3 seconds of animation is constant color

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

#make just the colors, plus traits of the song, inheritable



def vector_field(pos, note_vectors):
    x, y = pos
    closest_note = min(note_vectors, key=lambda note: abs(note[0] - y))  # Find closest beat time to 'y'
    note = closest_note[1]  # Get the note value for the closest beat time
    beat_time = closest_note[0]  # Get the corresponding beat time

    # Define the direction of the streamlines based on both note value and beat time
    direction = np.sin(note * y) * RIGHT + np.cos(beat_time * x) * UP
    return direction


class colorChanger(Scene):
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
    def construct(self):
        audio_file_name = preview_request()
        y, sr = librosa.load(audio_file_name)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        song_time = librosa.get_duration(y=y, sr=sr)
        percent_through_song = beat_times/song_time


        # num_to_take_from_y_1 = ((percent_through_song-0.02)*y.size).astype(int)
        # num_to_take_from_y_2 = ((percent_through_song-0.01)*y.size).astype(int)
        # num_to_take_from_y_3 = ((percent_through_song+0.00)*y.size).astype(int)

        # # Normalize the audio values to generate RGB color channels
        # r = norm_for_color(y[num_to_take_from_y_1]).astype(int)
        # b = norm_for_color(y[num_to_take_from_y_2]).astype(int)
        # g = norm_for_color(y[num_to_take_from_y_3]).astype(int)

        # zip_obj = zip(r,b,g)
        # color_list = list(zip_obj)

        # vectorized_function = np.vectorize(rgb_to_hex, signature='(n)->()')
        # colors = vectorized_function(np.array(color_list))
        # formatted_colors = ['#' + str(color) for color in colors]

        # cues = np.diff(beat_times) # not used
        
        notes = extract_notes(y, sr, beat_times)
        note_vectors = list(zip(beat_times, notes))

        speed_factor= tempo/40 

        stream_lines = StreamLines(lambda pos: vector_field(pos, note_vectors), stroke_width=3, max_anchors_per_line=30,
            virtual_time=song_time,
            three_dimensions=False,
            padding=1)
        self.add(stream_lines)
        self.add_sound(audio_file_name)
        stream_lines.start_animation(warm_up=False, flow_speed=speed_factor)
        self.wait(30)


# Goal for the animation:
# Speed = tempo (check)
# Colors = harmonic/percussive? more harmonic = more blue more percussive = more red?
# Shape = vector field = notes over time, using note map







