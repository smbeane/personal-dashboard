import requests
from datetime import datetime

def getDays():
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
  
  return days

#returns:
#  todays_weather: string = one of the weather choices in dashboard
#  low_temps:      int[]  = ints representing low temps for the next given days
#  high_temps:     int[]  = ints representing high temps for the next given days
def getWeatherVals(latitude, longitude):
  weather = getWeatherJSON(latitude, longitude)
  if(weather == "Weather API Error"):
    return "Weather API Err", [], []
  
  high_temps = weather["daily"]["temperature_2m_max"]
  low_temps = weather["daily"]["temperature_2m_min"]
  weather_code = weather["daily"]["weather_code"][0]
  wind_speed = weather["daily"]["wind_speed_10m_max"]

  if(weather_code < 50 and wind_speed[0] > 15):
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
  
  high_temps = [int(temp) for temp in high_temps]
  low_temps = [int(temp) for temp in low_temps]

  return todays_weather, low_temps, high_temps

def getWeatherJSON(latitude, longitude):

  head = { "Content-Type" : "application/json"}
  url = "https://api.open-meteo.com/v1/forecast"
  head= {"Content-Type": "application/json"}
  params = {
    "latitude": latitude,
    "longitude": longitude,
    "timezone": "America/New_York",
    "temperature_unit": "fahrenheit",
    "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "wind_speed_10m_max"],
    "wind_speed_unit": "mph",
    "forecast_days": 5
  }

  weather = requests.get(url=url, headers=head, params=params).json()
  try: 
    if(weather["error"] == True):
      return "Weather API Error"
    else: return weather
  except KeyError:
    return weather
  
#returns:
# dayTime: string = day and time in format "Mon 00:00 AM"
# date:    string = date in format "Jan 01 2025"  
# seconds: string = current amount of seconds 
def getTimeAndDate():
  currTime = datetime.now()

  weekday = currTime.strftime("%a")
  month = currTime.strftime("%b")
  year = currTime.strftime("%Y")
  day = currTime.strftime("%d")
  hour = currTime.strftime("%I")
  minute = currTime.strftime("%M")
  seconds = currTime.strftime("%S")
  am_pm = currTime.strftime("%p")

  dayTime = " ".join([weekday, ":".join([hour, minute]), am_pm])
  date = " ".join([month, day, year])

  return dayTime, date, seconds
