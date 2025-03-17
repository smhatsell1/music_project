#LIBRARIES
from manim import *
import os
import subprocess

#CODE FOR ANIMATION
from video_anim import circleAnim  

def render_manim_scene(song_path):
    """Render a Manim animation scene based on a given 
    song path and save the output as an MP4 file.
    @param: 
        song_path (str): The path to the song file
    
    @returns: 
        str: The path to the generated MP4 file containing the animation.
    """

    # ensure the output directory exists
    if not os.path.exists('static/animations'):
        os.makedirs('static/animations')

    # extract song title from filename
    output_directory = os.path.join(os.path.dirname(__file__), 'static/animations')
    song_title = os.path.basename(song_path).split("_")[0]
    output_file = os.path.join(output_directory, f"{song_title}.mp4")

    # define the output file path
    song_title = song_path.split("/")[2].split("_")[0]
    output_file = os.path.join(output_directory, f"{song_title}.mp4")

    os.environ["SONG_PATH"] = song_path

    # construct the Manim command with the correct output path
    command = [
        "manim", 
        "-ql",  # quality: low
        "video_anim.py",  # Python file containing the scene
        "circleAnim",  # Name of the scene class to render
        "-o", output_file  # Output path for the animation
    ]
    
    # print the command for debug purposes
    # print("Running Manim command:", " ".join(command)) #UNCOMMENT FOR DEBUG
    
    # run the command
    subprocess.run(command)

    # return the final MP4 file path
    return output_file


