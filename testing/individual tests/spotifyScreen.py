#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
import time
import RPi.GPIO as GPIO
from PIL import Image
import urllib.request
from datetime import datetime, timedelta

from SpotifyClass import SpotifyUser
from letters import letters_temp



REFRESH_TOKEN = "AQAr38rlNlnrhb-KftJwfNyu5zLukmj_WidoIswV-lg44-wKgeogwcAn1ZclmTKco_1o9nkBX1BGvC949nioUuJ9LMv7WhzfL1DyKEhxl-tYN1r6weusLY3rV5qRRd8H2ik"
CLIENT_ID = "1d63c5cfdfd24410b1630dfb6a6d0e48"
CLIENT_SECRET = "d316ab44da0d48f8aa238608bae2cd38"
backPin = 18
pausePin = 22
nextPin = 35
pressTime = 0
user = SpotifyUser(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(backPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pausePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(nextPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
def buttonRelease(channel):
    global pressTime
    if(channel == backPin):
        print("Back Released")
        user.alterPlayback("previous")
        user.playbackState = user.updatePlayback()
    elif(channel == nextPin):
        print("Next Released")
        user.alterPlayback("next")
        user.playbackState = user.updatePlayback()
    elif(channel == pausePin):
        if(GPIO.input(pausePin) == 1):
            print("Pause Released")
            releaseTime = datetime.now()
            print(f"Hold Time: {releaseTime - pressTime}")
            if(releaseTime - pressTime >= timedelta(seconds=1.5)):
                print("Button Held")
            else:
                print("Unpaused")
        else: 
            print("Pause Pressed")
            pressTime = datetime.now()
            print(pressTime)
            
        
    else:
        print("??? Released")

def destroy():
	GPIO.cleanup()

class SpotifyDisplay(SampleBase):
    def __init___(self, *args, **kwargs):
        super(SpotifyDisplay, self).__init__(*args, **kwargs)
    
    def run(self):
        setup()
        
        previousPlayback = {}
        loopCount = 0
        max_chars = 9
        
        canvas = self.matrix.CreateFrameCanvas()
       
        lastPressed = 0
      
        
        GPIO.add_event_detect(backPin, GPIO.RISING, callback=buttonRelease, bouncetime=200)
        GPIO.add_event_detect(nextPin, GPIO.RISING, callback=buttonRelease, bouncetime=200)
        GPIO.add_event_detect(pausePin, GPIO.BOTH, callback=buttonRelease, bouncetime=200)
        
        #GPIO.add_event_detect(pausePin, GPIO.FALLING, callback=buttonPress, bouncetime=200)
        while True:
            if user.device == 0:
                print("No Device Playing")
                canvas.Fill(0, 0, 0)
                self.setText("no devices on", 7, 13, 16, canvas)
                canvas = self.matrix.SwapOnVSync(canvas)
                
                time.sleep(5)
                print("Checking for Device Update")
                user.playbackState = user.updatePlayback()
                if(user.playbackState != "Not Playing"):
                    user.device = user.playbackState['device']['id']
                else: 
                    user.device = 0
                print("Device Updated")
                continue

            '''if GPIO.input(backPin) == 0:
                print("Back Pressed")
                user.alterPlayback("previous")
                user.playbackState = user.updatePlayback()
                time.sleep(0.5)
            elif GPIO.input(nextPin) == 0:
                print("Next Pressed")
                user.alterPlayback("next")
                user.playbackState = user.updatePlayback()
                time.sleep(0.5)
            elif GPIO.input(pausePin) == 0:
                print("Pause/Play Pressed")
                timeheld = 0
                while True:
                    if GPIO.input(pausePin) == 1:
                        print("Pause/Play Released")
                        break
                    elif timeheld >= 2:
                        break
                    time.sleep(0.05)
                    timeheld += 0.05
                if(timeheld >= 2):
                    print("Should show pages screen")
                else:
                    if(user.playbackState["is_playing"]):
                        user.alterPlayback("pause")
                    else:
                        user.alterPlayback("play")
                        user.playbackState = user.updatePlayback()
                    
                print(f"Timeheld: {timeheld}")
            '''
            time.sleep(0.05)
            if loopCount >= 60:
                print("Updating Playback")
                user.playbackState = user.updatePlayback()
                if(user.playbackState != "Not Playing"):
                    user.device = user.playbackState['device']['id']
                else: 
                    user.device = 0
                
                loopCount = 0
                print("Playback Updated")
            if(loopCount % 20 == 0):
                print("Updating Display")
                if (not previousPlayback or previousPlayback["item"]["name"] != user.playbackState["item"]["name"]):
                    canvas.Fill(0, 0, 0)
                    currentSong = user.playbackState["item"]["name"].lower() + "   "
                    currentArtist = user.playbackState["item"]["artists"][0]["name"].lower() + "   "
                    previousPlayback = user.playbackState
                    albumCover = user.playbackState["item"]["album"]["images"][0]["url"]
                    self.setBubbles(0, canvas)
                    
                self.setImage(albumCover, canvas)

                # calculate progress bubbles number
                song_duration = user.playbackState["item"]["duration_ms"]
                progress = user.playbackState["progress_ms"]
                bubbles_filled = int(progress / song_duration * 99)
                
                self.setBubbles(bubbles_filled, canvas)
                self.setText(currentSong, 27, 6, 9, canvas)
                self.setText(currentArtist, 27, 13, 9, canvas)
                
                if len(currentSong) > 12:
                    currentSong = currentSong[1:] + currentSong[0]
                if len(currentArtist) > 12:
                    currentArtist = currentArtist[1:] + currentArtist[0]
                
                canvas = self.matrix.SwapOnVSync(canvas)
                print("Display Updated")
                
            loopCount += 1
            
    
    
    def setImage(self, albumCover, canvas):
        urllib.request.urlretrieve(albumCover, "/home/smbeane5235/spotify/testing/albumCover.png")
        image = Image.open("/home/smbeane5235/spotify/testing/albumCover.png")
        image = image.resize((24,24))
    
        if(image.mode != "RGB"):
            image = image.convert("RGB")
        imageData = image.getdata() 
        allpixels = list(image.getdata())
        image.save("resizedAlbumCover.png")
        for y in range(0, 24):
            for x in range(0, 24):
                canvas.SetPixel(x + 2, y + 4, allpixels[y * 24 + x][0], allpixels[y * 24 + x][2], allpixels[y * 24 + x][1]) 
    
    def setBubbles(self, bubblesFilled, canvas):
        bubbleCount = 0
        for x in range(0, 35):
            for y in range(0, 5):
                if (y == 0 or y == 4 or x == 0 or x == 34):
                    canvas.SetPixel(x + 27, y + 21, 255, 255, 255)
                else: 
                    if(bubbleCount < bubblesFilled):
                        canvas.SetPixel(x + 27, y + 21, 255, 255, 255)
                        bubbleCount += 1
                    else: 
                        canvas.SetPixel(x + 27, y + 21, 0, 0, 0)
                        
    def setText(self, text, start_x, start_y, max_chars, canvas):
        char_count = 0
        for char in text:
            if char not in letters_temp:
                continue
            if char_count >= max_chars:
                break
            for y in range(5):
                for x in range(3):
                    if(letters_temp[char][y][x] == 1):
                         canvas.SetPixel(start_x + x + char_count * 4, start_y + y, 255, 255, 255)
                    else:
                        canvas.SetPixel(start_x + x + char_count * 4, start_y + y, 0, 0, 0)

            char_count += 1
            
if __name__ == "__main__":
    spotify_display = SpotifyDisplay()
    if(not spotify_display.process()):
        spotify_display.print_help()
