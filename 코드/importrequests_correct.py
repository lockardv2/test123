import requests
import json
from datetime import datetime

API_KEY = 'YOUR_API_KEY'  # Enter your OpenWeatherMap API key here
city = 'Seoul'
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=en&units=metric'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    # Parse weather information
    weather_data = {
        'city': city,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'weather_info': {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity']
        }
    }

    # Save as JSON file
    filename = f'weather_{city.lower()}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=2)

    print(f"=== Current Weather in {city} ===")
    print(f"Weather: {weather_data['weather_info']['description']}")
    print(f"Temperature: {weather_data['weather_info']['temperature']}°C")
    print(f"Feels like: {weather_data['weather_info']['feels_like']}°C")
    print(f"Min temperature: {weather_data['weather_info']['temp_min']}°C")
    print(f"Max temperature: {weather_data['weather_info']['temp_max']}°C")
    print(f"Humidity: {weather_data['weather_info']['humidity']}%")
    print(f"\nWeather information has been saved to '{filename}'.")
else:
    error_data = {
        'city': city,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'error': "Couldn't retrieve weather information.",
        'status_code': response.status_code
    }

    filename = f'weather_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(error_data, f, ensure_ascii=False, indent=2)

    print("Couldn't retrieve weather information.")
    print(f"Error details have been saved to '{filename}'.")