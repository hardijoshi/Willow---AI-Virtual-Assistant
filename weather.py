import requests

def get_weather(city):
    api_key = "WDjl99LABMYDlJoOdzCXMmo4eVsFPIgs"
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        temperature = data['data']['values']['temperature']
        cloud_cover = data['data']['values']['cloudCover']
        description = get_description(cloud_cover)
        return temperature, description
    else:
        return None, None

def get_description(cloud_cover):
    if cloud_cover == 0:
        return "Clear skies"
    elif 0 < cloud_cover <= 0.25:
        return "Few clouds or scattered clouds"
    elif 0.25 < cloud_cover <= 0.75:
        return "Partly cloudy"
    else:
        return "Mostly cloudy to overcast"

if __name__ == "__main__":
    city = input("Enter the name of the city: ")
    temperature, description = get_weather(city)
    if temperature is not None and description is not None:
        print(f"Temperature: {temperature}°C")
        print(f"Description: {description}")
    else:
        print("Failed to fetch weather data.")
