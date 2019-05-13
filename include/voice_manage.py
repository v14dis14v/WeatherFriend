import speech_recognition as sr
import gtts
from pygame import mixer

weatherFriend = r"погода друг"
byе = r"погода друг пока"
new_city = r"сменить город"
new_units = r"сменить единицу измерения"

def talk(words):

    phrase = gtts.gTTS(words, lang='ru')
    phrase.save("data/latest_data.mp3")

    mixer.init()
    mixer.music.load("data/latest_data.mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass


def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Говорите")
        # r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)

    try:
        transformation = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали", transformation)
    except sr.UnknownValueError:
        talk("Я вас не поняла, мой капитан!")
        transformation = command()

    return transformation
