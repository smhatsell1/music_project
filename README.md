# Music Visualization Project

Winter 2025 | PIC 16B | Group Project | Sarah Burnett

**Group members**: Sophia Hatsell, Caroline Ives, May Jiang

---
## Description
This project is designed to make an audio reactive animation of music based off a 30 second snippet of any given song. The final product is a Flask app that is run from the command line. The user is prompted to search for a song and downloads a 30-second preview clip from Deezer and then a simple animation is generated. The Python library, Librosa, is used to determine the songs pitches, tempo and volumes. This data is used to create a short animation with Manim, where colors change and a circle shifts and grows corresponding to the music. The final products is integrated with Flask to make a dynamic website. The song is saved as an mp3 file and the animation as an mp4 is saved to the user's machine.
## Using the project
**Necessary Packages**: Manim, Librosa, Requests, Numpy, Flask . 

These may installed using a package manager of your choice. See the versions below:

- requests: 2.32.3
- librosa: 0.10.2.post1
- manim: 0.18.1
- manimpango: 0.6.0    
- numpy: 1.26.2
- flask: 3.0.0

**Run**: In the command line, navigate to the MusicVis-Final folder and run the command `python app.py`.
