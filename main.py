from gtts import gTTS
from playsound import playsound
import openai
import os
import numpy as np
import speech_recognition as sr

PATH = os.path.dirname(os.path.abspath(__file__))
MP3_FILE = "speak.mp3"
OPEN_API_KEY = "OPEN_AI_KEY"
ERROR_MESSAGE = "Sorry, I cannot understand what you say"


def speak(text_string):
    word = gTTS(text_string)
    word.save(MP3_FILE)
    sound_file = PATH + "/" + MP3_FILE
    playsound(sound_file)
    os.remove(sound_file)


def ask(text_string):
    openai.api_key = OPEN_API_KEY
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=text_string,
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    results = np.array(response["choices"])
    if results.size > 0:
        return results[0].text
    else:
        return ""


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        words = r.recognize_google(audio)
        print(words)
        print("You: " + words)
        answer = ask(words)
        print("Robot: " + answer.replace("\n", ""))
        speak(answer)
    except sr.UnknownValueError:
        speak(ERROR_MESSAGE)
    except sr.RequestError:
        speak(ERROR_MESSAGE)


if __name__ == '__main__':
    welcome_message = "Hello, How may I help you today?"
    print(welcome_message)
    speak(welcome_message)
    while True:
        listen()
