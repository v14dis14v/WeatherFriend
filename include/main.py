import requests
import json
import os
import voice_manage as vm
from py_translator import Translator
import settings


api_url = "http://api.openweathermap.org/data/2.5/weather"
answer = "Сейчас в городе {} температура {} градусов {}"
greeting = "В каком городе вы находитесь?"
# go up one level
os.chdir(os.path.abspath(os.path.join("src", "../..")))


#checking for previously entered personal data
if os.path.exists("data/personal_information.json"):
    # if the file exists, then read the data from there
    with open("data/personal_information.json") as pd:
        data = json.load(pd)
        city = data['city']
        units = data['units']

else:
    # otherwise create db and write parameters there
    city = settings.add_city()
    units = 'metric'
params = {
    'q':  city,
    'appid': 'bcb1fd74d24a5fd0662b7f7da023f505',
    'units': units
}

while True:
    vm.talk("Чего желаете?")
    now = vm.command()

    if now == vm.byе:
        vm.talk("Пока, пока, мой дружочек!")
        break

    elif now == vm.weatherFriend:
        req = requests.get(api_url, params=params)
        data = req.json()
        rus_city = Translator().translate(text=city, dest="ru").text

        if params['units'] == 'metric':
            local_unit = " цельсия"
        elif params['units'] == 'imperial':
            local_unit = " фаренгейт"
        else:
            local_unit = " кельвина"

        print(answer.format(rus_city, data["main"]["temp"], local_unit))
        vm.talk(answer.format(rus_city, data["main"]["temp"], local_unit))

    elif now == vm.new_city:
        city = settings.add_city()
    elif now == vm.new_units:
        params['units'] = settings.add_units(city)



