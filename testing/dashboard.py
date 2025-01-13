from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
import requests
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from PIL import Image

from SpotifyClass import SpotifyUser
from displayFunctions import setImage, setBubbles, setText, setDivider
from weatherDateFunctions import getDays, getTimeAndDate, getWeatherVals

DASHBOARD_STATES = ["Home", "Weather", "Spotify", "Pages"]

REFRESH_TOKEN = "AQAr38rlNlnrhb-KftJwfNyu5zLukmj_WidoIswV-lg44-wKgeogwcAn1ZclmTKco_1o9nkBX1BGvC949nioUuJ9LMv7WhzfL1DyKEhxl-tYN1r6weusLY3rV5qRRd8H2ik"
CLIENT_ID = "1d63c5cfdfd24410b1630dfb6a6d0e48"
CLIENT_SECRET = "d316ab44da0d48f8aa238608bae2cd38"

BACK_PIN = 18
PAUSE_PIN = 22
NEXT_PIN = 35


class Dashboard(SampleBase):
  def __init__(self, *args, **kwargs):
    super(Dashboard, self).__init__(*args, **kwargs)
    self.mode = "Home"
    self.user = SpotifyUser(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    self.pressTime = 0
  
  def run(self):
    canvas = self.matrix.CreateFrameCanvas()
    sleepTime = 300
    currSleepTime = 0
    lastMode = self.mode
    while True:
      if(lastMode == self.mode and sleepTime > currSleepTime):
        pass
      elif self.mode == "Home":
        currSleepTime = 0
        lastMode = self.mode

        dayTime, date, seconds = getTimeAndDate()
        setText(canvas, dayTime, 0, 0, 16, 255, 255, 255)
        setText(canvas, date, 0, 6, 16, 255, 255, 255)
          
        canvas = self.matrix.SwapOnVSync(canvas)
        print("Updated!")
        sleepTime = 60 - int(seconds)

      elif self.mode == "Weather":
        currSleepTime = 0
        lastMode = self.mode

        todays_weather, low_temps, high_temps = getWeatherVals(40.4249916, -86.9063623)
        days = getDays()
        image = Image.open("/home/smbeane5235/spotify/images/Icons/" + todays_weather + ".png")
        setImage(canvas, image, 24, 18, 0, 0)

        setText(canvas, "today", 2, 19, 5, 255, 255, 255)
        setText(canvas, "|".join([str(low_temps[0]), str(low_temps[1])]), 2, 25, 5, 255, 255, 255)
        setDivider(canvas, 24, 3, 28, 63, 81, 181)

        for i in range(1, 5):
          low_high = "|".join([str(low_temps[i]), str(high_temps[i])])
          full_text = " ".join([days[i], low_high])

        canvas = self.matrix.SwapOnVSync(canvas)
        sleepTime = 300
      
      elif self.mode == "Spotify":
        lastMode = self.mode
        currSleepTime = 0

        setText(canvas, "spotify", 0, 0, 10, 255, 255, 255)

      elif self.mode == "Pages":
        lastMode = self.mode
        currSleepTime = 0

        setText(canvas, "Pages", 0, 0, 255, 255, 255)

      else:
        lastMode = self.mode
        currSleepTime = 0

        setText(canvas, "No clue", 0, 0, 255, 255, 255)
      
      time.sleep(1)
      currSleepTime += 1

  def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  def destroy(self):
    self.canvas.Fill(0, 0, 0)
    self.canvas = self.matrix.SwapOnVSync(self.canvas)
    GPIO.cleanup()

  def buttonActions(self, channel):
    #Back button was released
    if(channel == BACK_PIN and self.mode == "Spotify"): 
      print("Back Pressed")
      self.user.alterPlayback("previous")
      self.user.updatePlayback()
    #Next button was released 
    elif(channel == NEXT_PIN and self.mode == "Spotify"): 
      print("Next Pressed")
      self.user.alterPlayback("next")
      self.user.updatePlayback()
    #Pause button was pressed
    elif(channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 0): 
      self.pressTime = datetime.now()
    #Pause button was released
    elif(channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 1): 
      releaseTime = datetime.now()
      holdTime = releaseTime - self.pressTime
      print(f"Pause Released, Hold Time: {holdTime}")
      if(holdTime >= timedelta(seconds=1.25)):
        print("Show Pages")
        self.mode = "Pages"
      elif(self.mode == "Spotify"):
        if(self.user.playbackState["is_playing"]):
          self.user.alterPlayback("pause")
        else:
          self.user.alterPlayback("play")
        self.user.updatePlayback()
    #???
    else:
      print("??? Pressed")



if __name__ == "__main__":
  dashboard = Dashboard()
  if(not dashboard.process()):
    dashboard.print_help()
  

