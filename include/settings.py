import voice_manage as vm
from py_translator import Translator
import json


greeting_city = "В каком городе вы находитесь?"
greeting_units = """Температура доступна в градусах Фаренгейта, Цельсия и Кельвина
                    \tДля температуры в градусах Фаренгейта скажите «Фаренгейт»
                    \tДля температуры в градусах Цельсия скажите «Цельсий»
                    \tДля температуры в Кельвинах скажите «Кельвин»."""


def add_city():
    while True:
        print(greeting_city)
        vm.talk(greeting_city)
        city = vm.command()
        vm.talk("Всё верно?")
        fast_ans = vm.command()
        if fast_ans == r"да":

            eng_city = Translator().translate(text=city.replace("-", " "), dest="en").text

            current_location = {
                'city': eng_city,
                'units': 'metric'
            }

            with open("data/personal_information.json", "w") as dp:
                json.dump(current_location, dp, indent=4)
            return eng_city


def add_units(city):
    while True:
        print(greeting_units)
        vm.talk(greeting_units)
        units = vm.command()
        vm.talk("Всё верно?")
        fast_ans = vm.command()
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
                'city': city,
                'units': units
            }

            with open("data/personal_information.json", "w") as dp:
                json.dump(current_location, dp, indent=4)
            return units