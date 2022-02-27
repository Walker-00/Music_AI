# modules import
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import requests
import json
# recognizer init
recognizer = speech_recognition.Recognizer()
# text to speech init
speaker = tts.init()
# speech rate for AI
speaker.setProperty("rate", 100)

# object for music
def music():
    global recognizer
    # get singer name from user's say
    speaker.say("Singer Name sir")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                # remove noise from user's say
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                # send user's audio data to google and get singer name
                singer = recognizer.recognize_google(audio)
                singer = singer.lower()
# get song name from user's say
                speaker.say("Song Name Sir")
                speaker.runAndWait()
# remove noise from user's say
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
# send user's audio data to google and get song name
                song = recognizer.recognize_google(audio)
                song = song.lower()
# making file with singer name and song name in the file
            with open(singer, 'w') as f:
                f.write(song)
                # requests for song lyrics
                r = requests.get('https://api.lyrics.ovh/v1/' + singer + "/" + song)
                s = json.loads(r.text)
                # sing the song lyrics
                speaker.say(str(s["lyrics"]))
                speaker.runAndWait()
# speech error except
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I don't understand Sir")
            speaker.runAndWait()

# object for greeting
def hello():
    speaker.say("hi")
    speaker.runAndWait()

# object for quite
def quilt():
    speaker.say("Bye, Sir")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "Music": music,
    "exit": quilt
}
# train the model with json file and map
assistant = GenericAssistant('music.json', intent_methods=mappings)
assistant.train_model()

# get voice message and send to google
while True:

    try:

        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
# Error except
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
