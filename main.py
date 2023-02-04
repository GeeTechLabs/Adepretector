from re import split
from flask import Flask, render_template, request, flash, redirect
from flask_bootstrap import Bootstrap
import test
import videoTester
import voiceAnalyzer
import time
# import pyaudio
import os
import wave
import uuid


UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/home2')
def home2():
    return render_template("index2.html")


@app.route('/qstn')
def phq():
    return render_template("phq9.html",data="Anxiety and Depression Detection")

@app.route('/expression') 
def expression():
    p=videoTester.exp()
    return render_template("face.html", data=p)


@app.route('/face') 
def face():
    return render_template("face.html", data="Anxiety and Depression Detection")

@app.route('/face2') 
def face2():
    return render_template("face2.html", data="Anxiety and Depression Detection")

@app.route('/voice')
def voice():
    return render_template("voice.html", data="Click on the Mic to Record")

@app.route('/voice2')
def voice2():
    return render_template("voice2.html", data="Click on the Mic to Record")


# @app.route('/voice_recording')
# def voice_recording():
#     CHUNK = 1024 
#     FORMAT = pyaudio.paInt16 #paInt8
#     CHANNELS = 2 
#     RATE = 44100 #sample rate
#     RECORD_SECONDS = 4
#     WAVE_OUTPUT_FILENAME = "output10.wav"

#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK) #buffer

#     #return render_template("voice.html", data = "Recording ....")

#     frames = []

#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         frames.append(data) # 2 bytes(16 bits) per channel

    

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()
#     return render_template("voice.html", data = "Done recording.")

@app.route('/voice_analyzer', methods=['POST'])
def voice_analyzer():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    user_file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if user_file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    print(full_file_name)
    user_file.save(full_file_name)

    # res = voiceAnalyzer.alalyzer(full_file_name)
    res2 = os.system('python test.py -f ' + full_file_name + ' > output.txt')
    result_file =  open("output.txt","r")
    #gender = ["male","female"]
    for line in result_file:
        if "Result:" in line:
            sound = line.split()
            res2 = sound[1]
    return render_template("voice.html", data=res2)

if __name__ == '__main__':
    # 
    app.run(host='0.0.0.0', ssl_context='adhoc')
