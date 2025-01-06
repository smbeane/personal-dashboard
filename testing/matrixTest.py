#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
import time

from SpotifyClass import SpotifyUser
from letters import letters_temp

from PIL import Image
import urllib.request

REFRESH_TOKEN = "AQAr38rlNlnrhb-KftJwfNyu5zLukmj_WidoIswV-lg44-wKgeogwcAn1ZclmTKco_1o9nkBX1BGvC949nioUuJ9LMv7WhzfL1DyKEhxl-tYN1r6weusLY3rV5qRRd8H2ik"
CLIENT_ID = "1d63c5cfdfd24410b1630dfb6a6d0e48"
CLIENT_SECRET = "d316ab44da0d48f8aa238608bae2cd38"

class SpotifyDisplay(SampleBase):
    def __init___(self, *args, **kwargs):
        super(SpotifyDisplay, self).__init__(*args, **kwargs)
    
    def run(self):
        user = SpotifyUser(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
        previousPlayback = {}
        loopCount = 0
        max_chars = 9
        
        
       
        while True:
            canvas = self.matrix.CreateFrameCanvas()
            
            if user.device == 0:
                self.setText("no devices on", 7, 13, 16, canvas);
                canvas = self.matrix.SwapOnVSync(canvas);
                
                time.sleep(5)
                
                user.playbackState = user.updatePlayback()
                if(user.playbackState != "Not Playing"):
                    user.device = user.playbackState['device']['id']
                else: 
                    user.device = 0
                
                continue;

            if (not previousPlayback or previousPlayback["item"]["name"] != user.playbackState["item"]["name"]):
                currentSong = user.playbackState["item"]["name"].lower() + "   "
                currentArtist = user.playbackState["item"]["artists"][0]["name"].lower() + "   "
                previousPlayback = user.playbackState
                albumCover = user.playbackState["item"]["album"]["images"][0]["url"]
                
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
            canvas = self.matrix.SwapOnVSync(canvas);
            time.sleep(1)
            if loopCount > 2:
                user.playbackState = user.updatePlayback()
                if(user.playbackState != "Not Playing"):
                    user.device = user.playbackState['device']['id']
                else: 
                    user.device = 0
                
                loopCount = 0
            else:
                loopCount += 1
            
    def setImage(self, albumCover, canvas):
        urllib.request.urlretrieve(albumCover, "/home/smbeane5235/spotify/testing/albumCover");
        image = Image.open("/home/smbeane5235/spotify/testing/albumCover")
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
            char_count += 1
            
if __name__ == "__main__":
    spotify_display = SpotifyDisplay()
    if(not spotify_display.process()):
        spotify_display.print_help()
