from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
from testing.helpers.letters import letters_temp

import requests
import time
from datetime import datetime
from PIL import Image

class SpotifyDisplay(SampleBase):
    def __init___(self, *args, **kwargs):
        super(SpotifyDisplay, self).__init__(*args, **kwargs)
    
    def run(self):
        head = { "Content-Type" : "application/json"}
        url = "https://api.open-meteo.com/v1/forecast"
        head= {"Content-Type": "application/json"}
        params = {
          "latitude": 41.682,
          "longitude": -85.9767,
          "timezone": "America/New_York",
          "temperature_unit": "fahrenheit",
          "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "wind_speed_10m_max"],
          "wind_speed_unit": "mph",
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
        wind_speed = weather["daily"]["wind_speed_10m_max"]

        print(wind_speed)
        print(weather_code)

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

        while True:
            canvas = self.matrix.CreateFrameCanvas()
            self.setImage(0, 0, "/home/smbeane5235/spotify/images/Icons/" + todays_weather + ".png", canvas)
            
            self.setText("today", 2, 19, 5, canvas)
            self.setText("|".join([str(int(low_temps[0])), str(int(high_temps[0]))]), 2, 25, 5, canvas)
            self.setDivider(24, canvas)
            for i in range(1, 5):
              low_high = "|".join([str(int(low_temps[i])), str(int(high_temps[i]))])
              full_text = " ".join([days[i], low_high])
              self.setText(full_text, 27, 3 + (i - 1) * 7, 9, canvas)
            
            
            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(900)
    
    
    def setImage(self, start_x, start_y, path, canvas):
        
        image = Image.open(path)
    
        if(image.mode != "RGB"):
            image = image.convert("RGB")
        imageData = image.getdata() 
        allpixels = list(image.getdata())
        
        for y in range(0, 18):
            for x in range(0, 24):
                canvas.SetPixel(start_x + x, start_y + y, allpixels[y * 24 + x][0], allpixels[y * 24 + x][2], allpixels[y * 24 + x][1]) 
    
    def setText(self, text, start_x, start_y, max_chars, canvas):
        char_count = 0
        text = text.lower()
        for char in text:
            if char not in letters_temp:
                continue
            if char_count >= max_chars:
                break
            for y in range(5):
                for x in range(3):
                    if(char == "|" and letters_temp[char][y][x] == 1):
                      canvas.SetPixel(start_x + x + char_count * 4, start_y + y, 63, 181, 81)
                    elif(letters_temp[char][y][x] == 1):
                        canvas.SetPixel(start_x + x + char_count * 4, start_y + y, 255, 255, 255)
            char_count += 1
      
    def setDivider(self, start_x, canvas):
        for y in range(28):
          canvas.SetPixel(start_x, y + 2, 63, 181, 81)
            
      
if __name__ == "__main__":
    spotify_display = SpotifyDisplay()
    if(not spotify_display.process()):
        spotify_display.print_help()



