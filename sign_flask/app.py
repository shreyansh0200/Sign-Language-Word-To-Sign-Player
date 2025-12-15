from flask import Flask, render_template, request, send_from_directory
import os
from recognizer import record_and_recognize
from matcher import correct_spelling, get_best_video_match

app = Flask(__name__)
VIDEO_FOLDER = "static/videos"

@app.route("/" )
def front_page():

    return render_template("front_page.html")    

@app.route("/index", methods=["GET", "POST"])
def index():
    video_name = None
    recognized_text = None
    corrected_text = None
    
    # Check if this is a Mic request or Text request
    if request.method == "POST":
        
        # 1. Microphone Input
        if "mic" in request.form:
            # This function blocks for 4 seconds
            recognized_text = record_and_recognize()
        
        # 2. Text Input
        elif "video_name" in request.form:
            recognized_text = request.form.get("video_name").strip().lower()

        # Process logic if we have text (from either source)
        if recognized_text:
            corrected_text = correct_spelling(recognized_text)
            video_name = get_best_video_match(corrected_text)

    return render_template(
        "index.html",
        video_name=video_name,
        recognized=recognized_text,
        corrected=corrected_text
    )

@app.route("/videos/<filename>")
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)