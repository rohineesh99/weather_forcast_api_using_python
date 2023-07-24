import requests
from dotenv import load_dotenv
import os, json
from dataclasses import dataclass

load_dotenv()
api_key = os.getenv('API_KEY')


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float
    pressure: float
    humidity: float
    country : str
    name : str


def get_lan_lon(city_name, state_code, country_code, API_key):
    resp = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}").json()
    a = resp[0]
    lat, lon = a.get('lat'), a.get('lon')
    return lat, lon


def current_weather(lat, lon, API_key):
    resp = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric").json()
    # print(json.dumps(resp, indent=4))
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=resp.get('main').get('temp'),
        pressure=resp.get('main').get('pressure'),
        humidity=resp.get('main').get('humidity'),
        country=resp.get('sys').get('country'),
        name=resp.get('name')
    )

    return data


def main(city_name, state_name, country_name):
    lat, lon = get_lan_lon(city_name, state_name, country_name, api_key)
    weather_data = current_weather(lat, lon, api_key)
    return weather_data

# if __name__ == "__main__":
#     lat,lon= get_lan_lon('Toronto','ON','Canada',api_key)
#     print(current_weather(lat,lon,api_key))
