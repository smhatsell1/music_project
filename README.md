# Music Visualization Project

Winter 2025 | PIC 16B | Group Project | Sarah Burnett

**Group members**: Sophia Hatsell, Caroline Ives, May Jiang

## Description
This project is designed to make an audio reactive animation based off a song the user is able to specify. The user is prompted to search for a song, then Deezer downloads a 30-second preview clip and finally a simple animation is generated. The Python library, Librosa, is used to determine the song's pitches, tempo and volumes. This data is used to create a short animation with Manim, where the background colors change and a circle expands and contracts corresponding to the music. The final products is integrated with Flask to make a dynamic website. The song is saved as an mp3 file and the animation as an mp4 is saved to the user's machine. A more detailed description of the details of this project may be found: https://smhatsell1.github.io/pic16-blog/posts/Final%20Write%20Up/

## Using the project
**Necessary Packages**: Manim, Librosa, Requests, Numpy, Flask . 

These may be installed using a package manager of your choice. See the versions below:

- requests: 2.32.3
- librosa: 0.10.2.post1
- manim: 0.18.1
- manimpango: 0.6.0    
- numpy: 1.26.2
- flask: 3.0.0

**Run**: In the command line, navigate to the MusicVis-Final folder and run the command `python app.py`.
