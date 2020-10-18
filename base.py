import sys
import cv2
import ffmpeg
import pyttsx3
import math

import matplotlib.pyplot as plt
import numpy as np
import wave

from PIL import Image
from gtts import gTTS

def syllableToImg(txt):
    vowels = "aeiouyæøåAEIOUYÆØÅ"
    pauses = ".,-"
    txt_list = txt.split()
    img_list = []
    for word in txt_list:
        for letter in word:
            if letter in vowels:
                img_list.append(letter)
            elif letter in pauses:
                img_list.append('-')
            else:
                img_list.append('-')

        img_list.append('-')
    img = Image.open('open.png')
    video = cv2.VideoWriter(filename='video.avi', fourcc=0, fps = 12, frameSize= img.size)
    for i in img_list:
        if i in vowels:
            video.write(cv2.imread('open.png'))
        if i in pauses or i:
            video.write(cv2.imread('closed.png'))
    video.release()

def google_tts(txt):
    tts = gTTS(text=txt, lang='no')
    tts.save('output.mp3')

def pyttsx3_tts(txt):
    tts_engine = pyttsx3.init()
    voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', voices[1].id)
    tts_engine.setProperty('rate', 125)
    tts_engine.say(txt)
    tts_engine.save_to_file(txt, 'output.mp3')
    tts_engine.runAndWait()

def add_audio():
    video_stream = ffmpeg.input('video.avi')
    audio_stream = ffmpeg.input('output.mp3')
    ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output('product.avi').overwrite_output().run()
    #ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output('product.avi').run()

def audio_plotter():
    soundfile = wave.open('output.mp3', 'r')
    frames = soundfile.getnframes()
    rate = soundfile.getframerate()
    duration = frames / float(rate)
    pictureframes = math.floor(12 * duration)
    signal = soundfile.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    print(duration, pictureframes)
    print(signal)
    plt.figure(1)
    plt.title("Waveform")
    plt.plot(signal)
    plt.show()
    

if __name__ == "__main__":
    #tts(sys.argv[1])
    pyttsx3_tts(sys.argv[1])
    #syllableToImg(sys.argv[1])
    #add_audio()
    audio_plotter()