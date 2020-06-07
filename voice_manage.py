import speech_recognition as sr
import pyttsx3
from py_translator import Translator

weatherFriend = ("погода", "погода друг", "друг погода", "какая сейчас погода", "какая сейчас погода за окном")
until = ("погода друг пока", "пока", " до свидания", "пока пока", " до скорого", "до скорой встречи")
new_city = ("сменить город", "поменяй город", "смени город", "поменять город")
new_units = ("сменить единицу измерения", "сменить шкалу", "поменять единицы", "сменить единицы",
             "сменить единицы измерения")

greeting_city = "В каком городе вы находитесь?"
greeting_units = """Температура доступна в градусах Фаренгейта, Цельсия и Кельвина
                    \tДля температуры в градусах Фаренгейта скажите «Фаренгейт»
                    \tДля температуры в градусах Цельсия скажите «Цельсий»
                    \tДля температуры в Кельвинах скажите «Кельвин»."""
time = ("время", "который час", "сколько времени", "сколько на часах")
date = ("дата", "который день", "какое сегодня число", "который месяц", "который день")
months = {'01': 'Января', '02': 'Февраля', '03': 'Марта', '04': 'Апреля', '05': 'Марта', '06': 'Июня',
          '07': 'Июля', '08': 'Августа', '09': 'Сентября', '10': 'Октября', '11': 'Ноября', '12': 'Декабря'}

def talk(words):

    voice_engine = pyttsx3.init()

    voice_engine.setProperty('voice', 'russian')
    voice_engine.setProperty('rate', 130)
    voice_engine.say(words)
    voice_engine.runAndWait()


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
        talk("Товарищ, я не понял, что вы сказали!")
        transformation = command()

    return transformation


def add_city():
    while True:
        print(greeting_city)
        talk(greeting_city)
        city = command()
        talk("Всё верно?")
        fast_ans = command()
        if fast_ans == r"да":

            eng_city = Translator().translate(text=city.replace("-", " "), dest="en").text

            current_location = {
                'q': eng_city,
                'units': 'metric'
            }
            return current_location

def add_units(city):
    while True:
        print(greeting_units)
        talk(greeting_units)
        units = command()
        talk("Всё верно?")
        fast_ans = command()
        if fast_ans == r"да":
            if units == "фаренгейт":
                units = "imperial"
            elif units == "цельсий":
                units = "metric"
            elif units == "кельвин":
                units = "default"
            else:
                add_units(city)

            current_location = {
                'q': city,
                'units': units
            }
            return current_location
