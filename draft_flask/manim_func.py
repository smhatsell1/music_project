from manim import *
import subprocess
import os

from video_anim import hsvAnim

def render_manim_scene():
    # Ensure the output directory exists
    output_directory = "static/animations"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_directory = os.path.join(os.path.dirname(__file__), 'static/animations')
    
    # Define the output file path
    output_file = os.path.join(output_directory, "create_circle.mp4")

    # Construct the Manim command with the correct output path
    command = [
        "manim", 
        "-pql",  # Preview quality (low)
        "manim_func.py",  # Path to the Python file containing the scene
        "hsvAnim",  # Name of the scene class to render
        "-o", output_file  # Output path for the rendered video
    ]
    
    # Print the command for debug purposes
    print("Running Manim command:", " ".join(command))
    
    # Run the command
    subprocess.run(command)

# Call the function to render the scene
if __name__ == '__main__':
	render_manim_scene()
