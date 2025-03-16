# import libraries
import os
from flask import Flask, render_template, request, redirect, url_for

# import our functions
from preview_request import preview_request
from generate_anim import render_manim_scene  


app = Flask(__name__)


# Folder to store the MP4 video
OUTPUT_DIR = "static/animations"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


#HOME PAGE
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


#GET SONG MP3
@app.route('/get_preview', methods=['POST'])
def get_preview():
    song_name = request.form.get('song_name')
    if song_name:
        audio_file_path = preview_request(song_name)

    else:
        return render_template('index.html', error="Song name is required!")
    
    video_file_path = render_manim_scene(audio_file_path)  

    if not video_file_path:
        return "Animation rendering failed.", 500

    return redirect(url_for('play_animation', video_file=os.path.basename(video_file_path)))


#PLAY ANIMATION 
@app.route('/play_animation')
def play_animation():
    video_file = request.args.get('video_file')

    if not video_file:
        return "No video found.", 404

    animation_path = f"animations/{video_file}"

    return render_template('play_animation.html', animation_path=animation_path)


# RUN FLASK APP
if __name__ == '__main__':
    app.run(debug=True)









