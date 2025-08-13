import requests
from typing import Dict, Any

URL = "https://api.open-meteo.com/v1/forecast"
HEADERS = {"Content-Type": "application/json"}

class OpenMeteoUser():
    def __init__(self, latitude: int, longitude: int, ):
        self.latitude = latitude
        self.longitude = longitude
        self.error = False
        
        self.update_data()
        

    def update_data(self) -> None:
        weather_data = self.get_data()
        self.todays_weather = weather_data["todays_weather"]
        
        if self.todays_weather == "Weather API Error":
            self.todays_low = None
            self.todays_high = None
            self.low_temps = None
            self.high_temps = None
            self.error = True
        else:
            self.todays_low = weather_data["low_temps"][0]            
            self.todays_high = weather_data["high_temps"][0]
            self.low_temps = weather_data["low_temps"][1:]
            self.high_temps = weather_data["high_temps"][1:]
            self.error = False
        
    def _get_data(self) -> Dict[str, Any]:
        weather_json = self.get_weather_json()
        if weather_json is None:
            return {
                "todays_weather": "Weather API Error",
                "low_temps": [],
                "high_temps": []
            }
        
        high_temps = weather_json["daily"]["temperature_2m_max"]
        low_temps = weather_json["daily"]["temperature_2m_min"]
        weather_code = weather_json["daily"]["weather_code"][0]
        wind_speed = weather_json["daily"]["wind_speed_10m_max"][0]

        if weather_code < 50 and wind_speed > 15:
            todays_weather = "wind"
        elif weather_code in (0, 1):
            todays_weather = "sun" 
        elif weather_code == 2:
            todays_weather = "partial clouds"
        elif weather_code in range(3, 11) or weather_code == 45:
            todays_weather = "clouds"
        elif weather_code in range(50, 70):
            todays_weather = "rain"
        elif weather_code in range(70, 80):
            todays_weather = "snow"
        else: 
            todays_weather = "thunder"
        
        high_temps = [int(temp) for temp in high_temps]
        low_temps = [int(temp) for temp in low_temps]

        return {
            "todays_weather": todays_weather,
            "low_temps": low_temps,
            "high_temps": high_temps
        }
    
    def _get_weather_json(self) -> Dict[str, Any] | None:
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": "America/New_York",
            "temperature_unit": "fahrenheit",
            "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "wind_speed_10m_max"],
            "wind_speed_unit": "mph",
            "forecast_days": 5
        }

        
        try:
            response = requests.get(url=URL, headers=HEADERS, params=params)
            response.raise_for_status()
            weather = response.json()

            if "error" in weather:
                return None
            else: return weather
        except requests.RequestException:
            return None
        

    
