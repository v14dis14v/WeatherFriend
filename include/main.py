import requests
import json
import os
import voice_manage as vm
from py_translator import Translator
from datetime import datetime

api_url = "http://api.openweathermap.org/data/2.5/weather"
answer = "Сейчас в городе {} температура {} градусов {}, а за окном {}. Ветер {} метров в секунду"
greeting = "В каком городе вы находитесь?"
# go up one level
os.chdir(os.path.abspath(os.path.join("src", "../..")))


#checking for previously entered personal data
if os.path.exists("data/personal_information.json"):
    # if the file exists, then read the data from there
    with open("data/personal_information.json") as pd:
        data = json.load(pd)
        params = data

else:
    params = vm.add_city()

def weather(params):
    params['appid'] = 'bcb1fd74d24a5fd0662b7f7da023f505'
    req = requests.get(api_url, params=params)
    data = req.json()
    rus_city = Translator().translate(text=data['name'], dest="ru").text
    print(data['weather'][0]['main'])
    weather_param = Translator().translate(text=data['weather'][0]['main'], dest="ru").text
    speed_wind = int(data['wind']['speed'])
    current_temp = int(data["main"]["temp"])

    if params['units'] == 'metric':
        local_unit = "цельсия"
    elif params['units'] == 'imperial':
        local_unit = "фаренгейт"
    else:
        local_unit = "кельвина"

    print(answer.format(rus_city, current_temp, local_unit, weather_param, speed_wind))
    vm.talk(answer.format(rus_city, current_temp, local_unit, weather_param, speed_wind))

    if 0 < current_temp < 10:
        vm.talk("Что-то прохладно на улице. Нужно пальто")
    elif 10 <= current_temp < 20:
        vm.talk("На улице нормальна погода. Нужна толстовка")
    elif 20 < current_temp:
        vm.talk("На улице жара. Выбери лёгкую одежду например шорты и футболка")
    elif -20 < current_temp <= 0:
        vm.talk("На улице холодно. Нужна зимняя куртка")
    elif current_temp <= -20:
        vm.talk("На улице мороз. Нужен пуховик")
    if weather_param == "Дождь":
        vm.talk("Нужен зонт")
    if speed_wind >= 8:
        vm.talk("и что-то на улице ветренно. Нужна ветровка")


while True:
    vm.talk("Чего желаете?")
    now = vm.command()

    if now in vm.until:
        vm.talk("Пока, пока, мой дружочек!")
        with open("data/personal_information.json", "w") as dp:
            json.dump(params, dp, indent=4)
        break

    elif now in vm.weatherFriend:
        weather(params)

    elif now in vm.new_city:
        params = vm.add_city()

    elif now in vm.new_units:
        params = vm.add_units(params['q'])

    elif now in vm.time:
        print(datetime.strftime(datetime.now(), "%H:%M:%S"))
        vm.talk("Сейчас " + datetime.strftime(datetime.now(), "%H:%M"))

    elif now in vm.date:
        print(datetime.strftime(datetime.now(), "%d.%m.%Y"))
        vm.talk("Сейчас " + datetime.strftime(datetime.now(), "%d") + vm.months[datetime.strftime(datetime.now(), "%m")])
