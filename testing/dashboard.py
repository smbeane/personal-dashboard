from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
import requests
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from PIL import Image

from SpotifyClass import SpotifyUser
from displayFunctions import setURLImage, setImage, setBubbles, setText, setDivider
from weatherDateFunctions import getDays, getTimeAndDate, getWeatherVals

DASHBOARD_STATES = ["Home", "Weather", "Spotify"]

REFRESH_TOKEN = "AQAr38rlNlnrhb-KftJwfNyu5zLukmj_WidoIswV-lg44-wKgeogwcAn1ZclmTKco_1o9nkBX1BGvC949nioUuJ9LMv7WhzfL1DyKEhxl-tYN1r6weusLY3rV5qRRd8H2ik"
CLIENT_ID = "1d63c5cfdfd24410b1630dfb6a6d0e48"
CLIENT_SECRET = "d316ab44da0d48f8aa238608bae2cd38"

BACK_PIN = 18
PAUSE_PIN = 22
NEXT_PIN = 35


class Dashboard(SampleBase):
  def __init__(self, *args, **kwargs):
    super(Dashboard, self).__init__(*args, **kwargs)
    self.mode = "Spotify"
    self.user = SpotifyUser(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    self.pressTime = 0
    self.previousPlayback = {}
    self.selection = -1
  
  def run(self):
    self.updateMatrix()
  
  def updateMatrix(self):
    canvas = self.matrix.CreateFrameCanvas()
    sleepTime = 300
    currSleepTime = 0
    lastMode = ""
    
    self.setupGPIO()
    GPIO.add_event_detect(BACK_PIN, GPIO.RISING, callback=self.buttonActions, bouncetime=200)
    GPIO.add_event_detect(NEXT_PIN, GPIO.RISING, callback=self.buttonActions, bouncetime=200)
    GPIO.add_event_detect(PAUSE_PIN, GPIO.BOTH, callback=self.buttonActions, bouncetime=200)
    while True:
      if(lastMode == self.mode and sleepTime > currSleepTime):
        pass
      elif self.mode == "Home":
        print("Mode == Home")
        currSleepTime = 0
        lastMode = self.mode
        self.selection = 0

        canvas.Fill(0, 0, 0)
        dayTime, date, seconds = getTimeAndDate()
        setText(canvas, dayTime.lower(), 0, 0, 16, 255, 255, 255)
        setText(canvas, date.lower(), 0, 6, 16, 255, 255, 255)
          
        canvas = self.matrix.SwapOnVSync(canvas)
        print("Updated!")
        sleepTime = 60 - int(seconds)

      elif self.mode == "Weather":
        print("Mode == Weather")
        currSleepTime = 0
        lastMode = self.mode
        self.selection = 1
        
        todays_weather, low_temps, high_temps = getWeatherVals(40.4249916, -86.9063623)
        days = getDays()
        image = Image.open("/home/smbeane5235/spotify/images/Icons/" + todays_weather + ".png")
        
        canvas.Fill(0, 0, 0)
        
        setImage(canvas, image, 24, 18, 0, 0)
        setText(canvas, "today", 2, 19, 5, 255, 255, 255)
        setText(canvas, "|".join([str(low_temps[0]).zfill(2), str(high_temps[0]).zfill(2)]), 2, 25, 5, 255, 255, 255)
        setDivider(canvas, 24, 2, 28, 63, 81, 181)

        for i in range(1, 5):
          low_high = "|".join([str(low_temps[i]).zfill(2), str(high_temps[i]).zfill(2)])
          full_text = " ".join([days[i], low_high])
          setText(canvas, full_text, 27, 3 + (i - 1) * 7, 9, 255, 255, 255)
        
        canvas = self.matrix.SwapOnVSync(canvas)
        sleepTime = 300
      
      elif self.mode == "Spotify":
        print("Mode == Spotify")
        lastMode = self.mode
        currSleepTime = 0
        self.selection = 2

        loopCount = 0
        
        #no devices active
        while loopCount <= 2:
          if self.user.device == 0 or self.user.playbackState == "Not Playing":
            print("No device playing")
            canvas.Fill(0, 0, 0)
            setText(canvas, "no devices on", 7, 13, 16, 255, 255, 255)
            
            self.user.updatePlayback()
            sleepTime = 2
          else:
            #first time through or song has changed
            print("Device is playing")
            if not self.previousPlayback or self.previousPlayback["item"]["name"] != self.user.playbackState["item"]["name"]: 
              canvas.Fill(0, 0, 0)
              currentSong = self.user.playbackState["item"]["name"] + "  "
              currentArtist = self.user.playbackState["item"]["artists"][0]["name"] + "   "
              self.previousPlayback = self.user.playbackState
              albumCover = self.user.playbackState["item"]["album"]["images"][0]["url"]
              song_duration = self.user.playbackState["item"]["duration_ms"]
              bubblesFilled = 0
              image = setURLImage(canvas, albumCover, 24, 24, 2, 4)
            else:  
              song_progress = self.user.playbackState["progress_ms"]
              bubblesFilled = int(song_progress / song_duration * 99)
              #song or artist greater than 9 max characters plus the two spaces added
              
              if len(currentSong) > 11:
                currentSong = currentSong[1:] + currentSong[0]

              if len(currentArtist) > 11: 
                currentArtist = currentArtist[1:] + currentArtist[0]

            setImage(canvas, image, 24, 24, 2, 4)
            setBubbles(canvas, bubblesFilled)
            setText(canvas, currentSong, 27, 6, 9, 255, 255, 255)
            setText(canvas, currentArtist, 27, 13, 9, 255, 255, 255)
            sleepTime = 0
            
            if(loopCount == 2):
              self.user.updatePlayback()
            
          canvas = self.matrix.SwapOnVSync(canvas)
          
          time.sleep(1)
          loopCount += 1

      elif self.mode == "Pages":
        print("Mode == Pages")
        lastMode = self.mode
        currSleepTime = 0
        
        canvas.Fill(0, 0, 0)
        print(self.selection)
        
        for index, state in enumerate(DASHBOARD_STATES):
          setText(canvas, state, 4, 2 + 7 * index, 10, 255, 255, 255)
        
        if(self.selection != -1):
          setText(canvas, "|", 1, 2 + 7 * self.selection, 1, 63, 81, 181)
        canvas = self.matrix.SwapOnVSync(canvas)
      
      else:
        print("Mode == ???")
        lastMode = self.mode
        currSleepTime = 0

        setText(canvas, "No clue", 0, 0, 255, 255, 255)
      
        canvas = self.matrix.SwapOnVSync(canvas)
      if(sleepTime > 0):
        time.sleep(1)
      currSleepTime += 1

  def setupGPIO(self):
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
    if(channel == BACK_PIN):
      print(self.mode)
      if(self.mode == "Spotify"): 
        print("Back Pressed")
        self.user.alterPlayback("previous")
        self.user.updatePlayback()
      if(self.mode == "Pages"):
        self.selection = self.selection - 1 if self.selection != 0 else 2 
    
    #Next button was released 
    elif(channel == NEXT_PIN): 
      if(self.mode == "Spotify"):
        print("Next Pressed")
        self.user.alterPlayback("next")
        self.user.updatePlayback()
      if(self.mode == "Pages"):
        self.selection = self.selection + 1 if self.selection != 2 else 0
    
    #Pause button was pressed
    elif(channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 0): 
      self.pressTime = datetime.now()
      
    #Pause button was released
    elif(channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 1): 
      releaseTime = datetime.now()
      holdTime = releaseTime - self.pressTime
      print(f"Pause Released, Hold Time: {holdTime}")
      if(holdTime >= timedelta(seconds=0.75) and self.mode != "Pages"):
        print("Show Pages")
        self.mode = "Pages"
      elif(self.mode == "Spotify"):
        if(self.user.playbackState["is_playing"]):
          self.user.alterPlayback("pause")
        else:
          self.user.alterPlayback("play")
        self.user.updatePlayback()
      elif(self.mode == "Pages"):
        self.mode = DASHBOARD_STATES[self.selection]
    
    #???
    else:
      print("??? Pressed")
      
    


if __name__ == "__main__":
  dashboard = Dashboard()
  if(not dashboard.process()):
    dashboard.print_help()
  

