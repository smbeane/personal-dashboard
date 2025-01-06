import requests
from datetime import datetime

head = { "Content-Type" : "application/json"}

url = "https://api.open-meteo.com/v1/forecast"
head= {"Content-Type": "application/json"}
params = {
  "latitude": 41.682,
	"longitude": -85.9767,
	"timezone": "America/New_York",
  "temperature_unit": "fahrenheit",
  "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "wind_speed_10m_max"],
  "forecast_days": 5
}

weather = requests.get(url=url, headers=head, params=params).json()

try:
  if(weather["error"] == True):
    print("Weather API Err")
    quit()
except: KeyError

current_time = datetime.now()
today = current_time.strftime("%A").lower()

match today:
  case "monday":
    days = ["mon", "tue", "wed", "thu", "fri"]
  case "tuesday":
    days = ["tue", "wed", "thu", "fri", "sat"]
  case "wednesday":
    days = ["wed", "thu", "fri", "sat", "sun"]
  case "thursday":
    days = ["thu", "fri", "sat", "sun", "mon"]
  case "friday":
    days = ["fri", "sat", "sun", "mon", "tue"]
  case "saturday":
    days = ["sat", "sun", "mon", "tue", "wed"]
  case "sunday":
    days = ["sun", "mon", "tue", "wed", "thu"]

high_temps = weather["daily"]["temperature_2m_max"]
low_temps = weather["daily"]["temperature_2m_min"]
weather_code = weather["daily"]["weather_code"][0]
wind_speed = weather["daily"]["wind_speed_10m_max"][0]

if(weather_code < 50 and wind_speed > 15):
  todays_weather = "wind"
elif(weather_code == 0 or weather_code == 1):
  todays_weather = "sun" 
elif(weather_code == 2):
  todays_weather = "partial clouds"
elif (weather_code >= 3 and weather_code <= 10 or weather_code == 45):
  todays_weather = "clouds"
elif (weather_code >= 50 and weather_code <= 69):
  todays_weather = "rain"
elif (weather_code >= 70 and weather_code <= 79):
  todays_weather = "snow"
else: 
  todays_weather = "thunder"

print("Weather: " + todays_weather)
print(days[0] + ": " + str(low_temps[0]) + "->" + str(high_temps[0]))
print(days[1] + ": " + str(low_temps[1]) + "->" + str(high_temps[1]))
print(days[2] + ": " + str(low_temps[2]) + "->" + str(high_temps[2]))
print(days[3] + ": " + str(low_temps[3]) + "->" + str(high_temps[3]))
print(days[4] + ": " + str(low_temps[4]) + "->" + str(high_temps[4]))


