import requests
import datetime
import random
import sys
import os
import smtplib
import webbrowser
import urllib
import pyttsx3
import speech_recognition as sr
import pyaudio
from PyDictionary import PyDictionary
#from pygame import mixer

#import ety
#from nltk.corpus import wordnet


def speak(audio):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[len(voices) - 1].id)

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 62)  # Slows down the speaking speed of the engine voice.

    print("  "+audio)
    engine.say(audio)
    engine.runAndWait()

def command():

    cmd = sr.Recognizer()
    with sr.Microphone() as source:
        cmd.adjust_for_ambient_noise(source)    # Adjusts the level to recieve voice even in case of noise in surroundings
        print('Listening..')
        audio = cmd.listen(source)
        try:
            query = cmd.recognize_google(audio,language='en-in')
            print('User: '+query+'\n')
        except sr.UnknownValueError:
            speak('Sorry ! I did not get that. Could you please type it out ?')
            query = str(input('Command: '))
    return query


def greeting():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12 :
        speak('Good Morning')
    if currentH >= 12 and currentH < 17 :
        speak('Good Afternoon')
    if currentH >= 17 and currentH != 0 :
        speak('Good Evening')
    
    
def find(name, path):
    for root, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def playOnYoutube(query_string):
    query_string = urllib.parse.urlencode({"search_query" : query})
    search_string = str("http://www.youtube.com/results?" + query_string)
    speak("Here's what you asked for. Enjoy!")
    webbrowser.open_new_tab(search_string)


def tellAJoke(self):
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept":"application/json"}
        )
    if res.status_code == 200:
        speak("Okay. Here's one")
        speak(str(res.json()['joke']))
    else:
        speak('Oops!I ran out of jokes')


