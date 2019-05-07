import requests
import json
import os

api_url = "http://api.openweathermap.org/data/2.5/weather"

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
    city = input("Enter your city: ")
    print("Temperature is available in Fahrenheit, Celsius and Kelvin units.\n"
          "\tFor temperature in Fahrenheit choose imperial.\n"
          "\tFor temperature in Celsius choose metric.\n"
          "\tFor temperature in Kelvin choose default.")
    units = input("Choose units: 'metric', 'imperial' or 'default' - ")
    current_location = {
        'city': city,
        'units': units
    }

    with open("data/personal_information.json", "w") as dp:
        json.dump(current_location, dp, indent=4)

params = {
    'q':  city,
    'appid': 'bcb1fd74d24a5fd0662b7f7da023f505'
}

if units != 'default':
    params['units'] = units

req = requests.get(api_url, params=params)
data = req.json()

with open ("tests/output_json.json", "r") as test_json:
    


answer = 'Current temperature in {} is {}'
print(answer.format(city, data["main"]["temp"]))