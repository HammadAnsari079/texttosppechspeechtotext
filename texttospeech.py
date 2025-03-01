from flask import Flask, render_template, request
from gtts import gTTS
import speech_recognition as sr
import os

# Create the app and ensure static directory exists
app = Flask(__name__)
os.makedirs('static', exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/text-to-speech", methods=["GET", "POST"])
def text_to_speech():
    if request.method == "POST":
        text = request.form["text"]
        if text.strip():
            try:
                speech = gTTS(text=text, lang="en", slow=False)
                speech.save("static/text.mp3")
                return render_template("tts.html", audio_file="static/text.mp3")
            except Exception as e:
                return render_template("tts.html", error=str(e), audio_file=None)
    return render_template("tts.html", audio_file=None)

@app.route("/speech-to-text", methods=["GET", "POST"])
def speech_to_text():
    if request.method == "POST":
        try:
            # Check if an audio file was uploaded
            if 'audio' in request.files:
                audio_file = request.files['audio']
                temp_file = "temp_audio.wav"
                audio_file.save(temp_file)
                
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_file) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="en-US")
                    os.remove(temp_file)  # Clean up
                    return render_template("stt.html", text=text)
            else:
                return render_template("stt.html", text="No audio file uploaded.")
        except Exception as e:
            return render_template("stt.html", text=f"Error: {str(e)}")
    return render_template("stt.html", text=None)

if __name__ == "__main__":
    app.run(debug=True)