# from manim import *
# import subprocess
# import os

# #GET SONG PATH
# from app import song_path

# from video_anim import hsvAnim

# def render_manim_scene(song_path):
#     # Ensure the output directory exists
#     output_directory = "static/animations"
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)

#     output_directory = os.path.join(os.path.dirname(__file__), 'static/animations')
    
#     # Define the output file path
#     song_title = song_path.split("/")[2].split("_")[0]
#     output_file = os.path.join(output_directory, f"{song_path}.mp4")

#     # Construct the Manim command with the correct output path
#     command = [
#         "manim", 
#         "-pql",  # Preview quality (low)
#         "manim_func.py",  # Path to the Python file containing the scene
#         "hsvAnim",  # Name of the scene class to render
#         "-o", output_file  # Output path for the rendered video
#     ]
    
#     # Print the command for debug purposes
#     print("Running Manim command:", " ".join(command))
    
#     # Run the command
#     subprocess.run(command)


from manim import *
import os
import subprocess
from video_anim import hsvAnim  

def render_manim_scene(song_path):
    # Ensure the output directory exists
    if not os.path.exists('static/animations'):
        os.makedirs('static/animations')

    # Extract song title from filename
    output_directory = os.path.join(os.path.dirname(__file__), 'static/animations')
    song_title = os.path.basename(song_path).split("_")[0]
    output_file = os.path.join(output_directory, f"{song_title}.mp4")

    # Define the output file path
    song_title = song_path.split("/")[2].split("_")[0]
    output_file = os.path.join(output_directory, f"{song_title}.mp4")

    os.environ["SONG_PATH"] = song_path

    # Construct the Manim command with the correct output path
    command = [
        "manim", 
        "-ql",  # Preview quality (low)
        "video_anim.py",  # Path to the Python file containing the scene
        "hsvAnim",  # Name of the scene class to render
        "-o", output_file  # Output path for the rendered video
    ]
    
    # Print the command for debug purposes
    print("Running Manim command:", " ".join(command))
    
    # Run the command
    subprocess.run(command)


    return output_file  # Return the final MP4 file path


