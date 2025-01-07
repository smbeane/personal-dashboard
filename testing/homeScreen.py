#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
import time
from datetime import datetime

from letters import letters_temp

import urllib.request


class SpotifyDisplay(SampleBase):
    def __init___(self, *args, **kwargs):
        super(SpotifyDisplay, self).__init__(*args, **kwargs)
    
    def run(self):
        while True:
            currTime = datetime.now()
            canvas = self.matrix.CreateFrameCanvas()
            
            weekday = currTime.strftime("%a")
            month = currTime.strftime("%b")
            year = currTime.strftime("%Y")
            day = currTime.strftime("%d")
            hour = currTime.strftime("%I")
            minute = currTime.strftime("%M")
            second = currTime.strftime("%S")
            am_pm = currTime.strftime("%p")
            
            dayTime = " ".join([weekday, ":".join([hour, minute]), am_pm])
            date = " ".join([month, day, year])
            
            self.setText(dayTime, 0, 0, 16, canvas)
            self.setText(date, 0, 6, 16, canvas)
            
            canvas = self.matrix.SwapOnVSync(canvas)
            print("Updated!")
            time.sleep(60 - int(second))
            
            
            
            
            
    
    
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
        text = text.lower()
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
