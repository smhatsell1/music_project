import numpy as np
import librosa
from manim import *
from colorsys import hsv_to_rgb
import os


def extract_max_pitches(y, sr, beat_times, duration=0.1):
    """Extracts the maximum pitch at each beat in a song. 
    @params:
        y (np.array): The audio time series
        sr (int): The sample rate of the audio
        beat_times (np.array): An array of beat_times in seconds
        duration (float): The duration (in seconds) of the segment around each beat
        
    @returns:
        np.array: An array of the maximum pitch values corresponding to each beat in beat_times.
    """
    pitches = []
    for time in beat_times:
        # extract a segment of audio around each timestamp
        start_sample = int(time * sr)
        end_sample = int((time + duration) * sr)
        segment = y[start_sample:end_sample]

        # get pitch
        pitches_segment, magnitudes = librosa.core.piptrack(y=segment, sr=sr)
        
        # get the maximum pitch from the frame with the highest magnitude
        max_pitch = np.max(pitches_segment)
        if max_pitch > 0:
            pitches.append(max_pitch)
        else:
            pitches.append(0) #no pitch heard
    
    return np.array(pitches)


def extract_max_volume(y, sr, beat_times, duration=0.1):
    """Extracts the maximum volume at each beat in a song. 
    @params:
        y (np.array): The audio time series
        sr (int): The sample rate of the audio
        beat_times (np.array): An array of beat_times in seconds
        duration (float): The duration (in seconds) of the segment around each beat
        
    @returns:
        np.array: An array of the maximum pitch volumes corresponding to 
                  each beat in beat_times as decibels.
    """
    volumes = []
    for time in beat_times:
        # extract a segment of audio around each timestamp
        start_sample = int(time * sr)
        end_sample = int((time + duration) * sr)
        segment = y[start_sample:end_sample]

        # get volume
        rms = librosa.feature.rms(y=segment)
        rms_db = librosa.amplitude_to_db(rms) #convert to decibels
        
        # get the maximum volume
        max_vol = np.max(rms_db)
        volumes.append(max_vol)
    
    return np.array(volumes)


def norm_to_n(array, n=1):
    """Normalizes an array of values to a range between 0 and n.
    @params: 
        array (np array): array of values to normalize
        n (int): Upper limit of the normalized range (default=1)
    
    @returns: np array normalized between 0-n
    """
    # get min and max of array
    min_val = np.min(array)
    max_val = np.max(array)
    
    # apply normalization formula
    normalized_array = (array - min_val) / (max_val - min_val) * n
    
    return normalized_array


def hsv_to_hex(hsv):
    """Converts a color from HSV (Hue, Saturation, Value) format to HEX format.
    @params:
        hsv (tuple): A tuple of (hue, saturation, value) where hue is in [0, 360], 
                     saturation and value are in [0, 100].
        
    @returns:
        str: The corresponding HEX color code as a string (e.g., 'ff5733').
    """
    h, s, v = hsv #unpack
    
    # convert 
    h = h/360
    s = s/100
    v = v/100
    
    r, g, b = hsv_to_rgb(h, s, v) #use colorsys
    
    # convert RGB to HEX
    hex_color = '{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
    
    return hex_color


class circleAnim(Scene):
    """A Manim scene that animates circles whose size and color change based on the beat and 
    characteristics of the song. The background color transitions dynamically with the music,
    and the circles grow/shrink based on the song's volume and pitch values at each beat.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # retrieve song_path from the environment variable
        self.song_path = os.getenv("SONG_PATH")
            
    def construct(self):
        # read in song data
        y, sr = librosa.load(self.song_path)

        # get beat_times
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_times = np.insert(beat_times, 0, 0) #prevent offset error
        
        # total song length
        song_time = librosa.get_duration(y=y, sr=sr)
    
        # define note map
        note_map = {
            'C':1,'C♯':1.5,
            'D':2,'D♯':2.5,
            'E':3,
            'F':4,'F♯':4.5,
            'G':5,'G♯':5.5,
            'A':6,'A♯':5.5,
            'B':7
        }

        # create color list
        pitches = extract_max_pitches(y, sr, beat_times)
        volumes = extract_max_volume(y, sr, beat_times)

        notes = librosa.hz_to_note(pitches, octave=False)
        note_vals = [note_map[note] for note in notes]

        H = norm_to_n(note_vals, 360) #hue from notes
        S = norm_to_n(volumes, 100) #saturation volumes
        B = norm_to_n(pitches, 100) #brightness from pitch

        # create list of 3-tuples
        zip_obj = zip(H,S,B)
        color_list = list(zip_obj)

        # convert to ManimColor
        vectorized_function = np.vectorize(hsv_to_hex, signature='(n)->()')
        list_of_colors = vectorized_function(np.array(color_list))
        list_of_colors = [ManimColor.from_hex('#'+color) for color in list_of_colors]
        
        # list cues for color change
        cues = np.diff(beat_times)
        
        # add music
        self.add_sound(self.song_path)

        # add background and initialize to first color
        background = FullScreenRectangle(fill_color=list_of_colors[0],  fill_opacity=1)
        self.add(background)

        # list of circle radii based on volume
        # normed to 4 to stay in frame
        rad = norm_to_n(S[1:],4)
        
        for i in range(len(cues)):
            # define previous circle
            circle_past = Circle(radius=rad[max(0,i-1)], color=BLACK, stroke_width=10)
            
            #define next circle
            circle_now = Circle(radius=rad[i]/100*4, color=BLACK, stroke_width=10)

            self.play(FadeToColor(background, color=list_of_colors[i]), #smoothly change background
                      Transform(circle_past, circle_now), #change circle size
                      run_time=cues[i] #take time to run
                     )
            self.remove(circle_past) #remove previous circle
