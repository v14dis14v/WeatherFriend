import speech_recognition as sr
import gtts
from pygame import mixer
import os


def talk(words):

    os.chdir(os.path.abspath(os.path.join("src", "../..")))

    talk = gtts.gTTS(words, lang='ru')
    talk.save("data/latest_data.mp3")

    mixer.init()
    mixer.music.load("data/latest_data.mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass

def comand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("You can say something ")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)

    try:
        transformation = r.recognize_google(audio).lower()
        print("Вы сказали", transformation)
    except sr.UnknownValueError:
        talk("Я вас не поняла, мой капитан!")
        transformation = comand()

    return transformation

comand()