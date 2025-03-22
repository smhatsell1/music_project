# Music Visualization Project

Winter 2025 | PIC 16B | Group Project | Sarah Burnett

**Group members**: Sophia Hatsell, Caroline Ives, May Jiang

---
## Description

    This project is designed to create music visualizations using audio data. The code prompts a user for a song title and downloads a 30-second preview clip from Deezer. Then, it uses Librosa to determine the songs pitches, tempo and volumes. This data is used to encode a short animation, where colors change and a circle shifts and grows corresponding to the music. The final products is integrated with Flask to make a dynamic website.
---
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
