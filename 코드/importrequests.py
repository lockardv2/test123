# Import requests library for making HTTP requests
import requests

# API key for OpenWeatherMap service - replace with your own key
API_KEY = 'YOUR_API_KEY'  # 실제 API 키로 교체하세요
# Specify the city to fetch weather information for
city = 'Seoul'
# Construct the URL for the weather API endpoint with parameters
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=kr&units=metric'

# Send GET request to the API
try:
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract weather description from the response
        weather = data['weather'][0]['description']
        # Extract temperature from the response
        temp = data['main']['temp']
        # Print the weather information for the city
        print(f"{city}의 현재 날씨: {weather}, 온도: {temp}°C")
    else:
        # Print error message if the request failed
        print(f"오류: {response.status_code} - 날씨 정보를 가져오지 못했습니다.")
except requests.exceptions.RequestException:
    # Print error message if there was a network error
    print("네트워크 오류: 인터넷 연결을 확인하세요.")
except (KeyError, ValueError):
    # Print error message if there was a JSON parsing error
    print("데이터 파싱 오류: 응답 데이터 형식이 올바르지 않습니다.")