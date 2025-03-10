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


def direction(pos, note_vectors):
    # Extract the x and y components from the pos array
    x_pos, y_pos = pos[0], pos[1]  # Assuming pos is an array like [x, y]

    # Find the closest note in time (based on x_pos)
    closest_note = min(note_vectors, key=lambda note: abs(note[0] - x_pos))  # Find closest beat time to 'x'
    
    note = closest_note[1]  # Note value for the closest beat time
    beat_time = closest_note[0]  # The corresponding beat time

    # Calculate the direction for the streamlines based on both beat time and note value
    direction_x = np.sin((note * x_pos)/2) * UR  # Movement up-right
    direction_y = np.cos((beat_time * y_pos)/2) * LEFT  # movement left

    # Return the resulting direction vector (combining the two components)
    return direction_x + direction_y


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
        
        notes = extract_notes(y, sr, beat_times)
        note_vectors = list(zip(beat_times, notes))

        speed_factor= tempo/40 

        stream_lines = StreamLines(lambda pos: direction(pos, note_vectors), stroke_width=3, max_anchors_per_line=40,
            virtual_time=song_time,
            three_dimensions=False,
            padding=1)
        self.add(stream_lines)
        self.add_sound(audio_file_name)
        stream_lines.start_animation(warm_up=False, flow_speed=speed_factor)
        self.wait(30)


# Goal for the animation:
# Speed = tempo
# Colors = harmonic/percussive? more harmonic = more blue more percussive = more red? Or volumes
# Shape = vector field = notes over time, using note map
# Number of stream lines
# 


#Possible improvements:
#Interpolation to fix janky movements



