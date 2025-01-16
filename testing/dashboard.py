from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
import requests
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from PIL import Image

from helpers.SpotifyClass import SpotifyUser
from helpers.displayFunctions import setURLImage, setImage, setBubbles, setText, setDivider
from helpers.weatherDateFunctions import getDays, getTimeAndDate, getWeatherVals

DASHBOARD_STATES = ["Home", "Weather", "Spotify"]
BACK_PIN = 18
PAUSE_PIN = 22
NEXT_PIN = 35

LAT = 40.4249916 
LONG = -86.9063623

class Dashboard(SampleBase):
  def __init__(self, *args, **kwargs):
    super(Dashboard, self).__init__(*args, **kwargs)
    self.currMode = "Home"
    self.lastMode = "Home"
    self.user = None
    self.pressTime = 0
    self.previousPlayback = {}
    self.selection = -1
    self.keepRunning = True
    self.canvas = None
   
  def homeScreen(self):
    while self.keepRunning:
      dayTime, date, seconds = getTimeAndDate()

      self.canvas.Fill(0, 0, 0)
      setText(self.canvas, dayTime.lower(), 0, 0, 16, 255, 255, 255)
      setText(self.canvas, date.lower(), 0, 6, 16, 255, 255, 255)

      sleepCounter = 0
      self.canvas = self.matrix.SwapOnVSync(self.canvas)
      while(self.keepRunning and sleepCounter < (60 - int(seconds)) * 10):
        time.sleep(0.1)
        sleepCounter += 1

  def weatherScreen(self):
    while self.keepRunning:  
      todays_weather, low_temps, high_temps = getWeatherVals(LAT, LONG)
      days = getDays()
      image = Image.open("/home/smbeane5235/spotify/images/Icons/" + todays_weather + ".png")

      self.canvas.Fill(0, 0, 0)
      setImage(self.canvas, image, 24, 18, 0, 0)
      setText(self.canvas, "today", 2, 19, 5, 255, 255, 255)
      setText(self.canvas, "|".join([str(low_temps[0]).zfill(2), str(high_temps[0]).zfill(2)]), 2, 25, 5, 255, 255, 255)
      setDivider(self.canvas, 24, 2, 28, 63, 81, 181)

      for i in range(1, 5):
        low_high = "|".join([str(low_temps[i]).zfill(2), str(high_temps[i]).zfill(2)])
        full_text = " ".join([days[i], low_high])
        setText(self.canvas, full_text, 27, 3 + (i - 1) * 7, 9, 255, 255, 255)
      
      self.canvas = self.matrix.SwapOnVSync(self.canvas)

      sleepCounter = 0
      while(self.keepRunning and sleepCounter < 18000):
        time.sleep(0.1)
        sleepCounter += 1  
    

  def spotifyScreen(self):
    loopCount = 0
    if self.user == None:
      self.user = SpotifyUser()
    while self.keepRunning:
      #checks for matrix update every second
      if loopCount % 30 == 0:
        print("Update Spotify Playback") 
        self.user.updatePlayback()
      
      if loopCount % 10 == 0:

        #updates the matrix every five seconds if not playing
        if (self.user.device == 0 or self.user.playbackState == "Not Playing"):
          print("No device playing")
          self.canvas.Fill(0, 0, 0)
          setText(self.canvas, "no devices on", 7, 13, 16, 255, 255, 255)
          self.canvas = self.matrix.SwapOnVSync(self.canvas)
        else:
          #if its the first time through or song has changed
          if not self.previousPlayback or self.previousPlayback["item"]["name"] != self.user.playbackState["item"]["name"]: 
            self.canvas.Fill(0, 0, 0)
            currentSong = self.user.playbackState["item"]["name"] + "  "
            currentArtist = self.user.playbackState["item"]["artists"][0]["name"] + "   "
            self.previousPlayback = self.user.playbackState
            albumCover = self.user.playbackState["item"]["album"]["images"][0]["url"]
            song_duration = self.user.playbackState["item"]["duration_ms"]
            bubblesFilled = 0
            image = setURLImage(self.canvas, albumCover, 24, 24, 2, 4)
          
          else:  
            self.canvas.Fill(0, 0, 0)
            song_progress = self.user.playbackState["progress_ms"]
            bubblesFilled = int(song_progress / song_duration * 99)
            if len(currentSong) > 11:
              currentSong = currentSong[1:] + currentSong[0]

            if len(currentArtist) > 11: 
              currentArtist = currentArtist[1:] + currentArtist[0]

          setImage(self.canvas, image, 24, 24, 2, 4)
          setBubbles(self.canvas, bubblesFilled)
          setText(self.canvas, currentSong, 27, 6, 9, 255, 255, 255)
          setText(self.canvas, currentArtist, 27, 13, 9, 255, 255, 255)

          self.canvas = self.matrix.SwapOnVSync(self.canvas) 

      #updates playback every 3 seconds
      
      time.sleep(0.1)
      if loopCount == 150:
        loopCount = 0
      else: 
        loopCount += 1


  def pagesScreen(self):
    while self.keepRunning:
      self.canvas.Fill(0, 0, 0)

      for index, state in enumerate(DASHBOARD_STATES):
        setText(self.canvas, state, 4, 2 + 7 * index, 10, 255, 255, 255)
          
      if(self.selection != -1):
        setText(self.canvas, "|", 1, 2 + 7 * self.selection, 1, 63, 81, 181)

      self.canvas = self.matrix.SwapOnVSync(self.canvas)

      while self.keepRunning:
        time.sleep(0.1)

  def run(self):
    self.canvas = self.matrix.CreateFrameCanvas()
    self.setupGPIO()
    while True:
      print(self.currMode)
      self.lastMode = self.currMode

      if self.currMode == "Home":
        print("Mode == Home")
        self.selection = 0

        self.homeScreen()
          
      elif self.currMode == "Weather":
        print("Mode == Weather")
        self.selection = 1
        
        self.weatherScreen()
      
      elif self.currMode == "Spotify":
        print("Mode == Spotify")
        self.selection = 2

        self.spotifyScreen()

      elif self.currMode == "Pages":
        print("Mode == Pages")

        self.pagesScreen()

      else:
        print("Mode == ???")

        setText(self.canvas, "No clue", 0, 0, 255, 255, 255)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

        while self.keepRunning:
          time.sleep(0.1)
      
      self.keepRunning = True

  def setupGPIO(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BACK_PIN, GPIO.FALLING, callback=self.buttonActions, bouncetime=200)
    GPIO.add_event_detect(NEXT_PIN, GPIO.FALLING, callback=self.buttonActions, bouncetime=200)
    GPIO.add_event_detect(PAUSE_PIN, GPIO.BOTH, callback=self.buttonActions, bouncetime=200)

  def destroy(self):
    self.canvas.Fill(0, 0, 0)
    self.canvas = self.matrix.SwapOnVSync(self.canvas)
    GPIO.cleanup()

  def buttonActions(self, channel):
    #Back button was released
    if(channel == BACK_PIN):

      if(self.currMode == "Spotify"): 
        print("Back Pressed")
        self.user.alterPlayback("previous")
        self.user.updatePlayback()

      elif(self.currMode == "Pages"):
        self.selection = self.selection - 1 if self.selection != 0 else 2 
        self.keepRunning = False
    
    #Next button was released 
    elif(channel == NEXT_PIN): 
      if(self.currMode == "Spotify"):
        print("Next Pressed")
        self.user.alterPlayback("next")
        self.user.updatePlayback()

      elif(self.currMode == "Pages"):
        self.selection = self.selection + 1 if self.selection != 2 else 0
        self.keepRunning = False
    
    #Pause button was pressed
    elif(channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 0): 
      self.pressTime = datetime.now()
      
    #Pause button was released
    elif(channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 1): 
      releaseTime = datetime.now()
      holdTime = releaseTime - self.pressTime
      
      #button was held, opens the pages tab
      if(holdTime >= timedelta(seconds=0.75) and self.currMode != "Pages"):
        self.currMode = "Pages"
        self.keepRunning = False

      elif(self.currMode == "Spotify"):
        if(self.user.playbackState["is_playing"]):
          self.user.alterPlayback("pause")
        else:
          self.user.alterPlayback("play")
        self.user.updatePlayback()
      elif(self.currMode == "Pages"):
        self.currMode = DASHBOARD_STATES[self.selection]
        self.keepRunning = False
    
    #???
    else:
      print("??? Pressed")
      
  


if __name__ == "__main__":
  dashboard = Dashboard()
  if(not dashboard.process()):
    dashboard.print_help()
  

