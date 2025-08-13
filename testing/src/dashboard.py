import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from PIL import Image
from typing import Tuple, Any

from samplebase import SampleBase
from pages.home_screen import HomeScreen
from pages.weather_screen import WeatherScreen
from pages.page_selection_screen import PageSelectionScreen

from lib.SpotifyClass import SpotifyUser
from lib.displayFunctions import (
    retrieve_url_image,
    setBubbles,
    setText
)
from lib.weatherDateFunctions import getDays, getWeatherVals

DASHBOARD_STATES = ["Home", "Weather", "Spotify"]
LEFT_PIN = 18
MIDDLE_PIN = 22
RIGHT_PIN = 35
WHITE = [255, 255, 255]
BLUE = [63, 81, 181]

LAT = 40.4249916
LONG = -86.9063623


class Dashboard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.currPage = None
        self.currMode = "Home"
        self.lastMode = "Home"
        self.user = None
        self.pressTime = 0
        self.previousPlayback = {}
        self.selection = -1
        self.keepRunning = True
        self.canvas = None
        self.home_screen = None

    #TODO change to individual file
    def spotifyScreen(self):
        loopCount = 0
        if self.user == None:
            self.user = SpotifyUser()

        while self.keepRunning:
            # checks for matrix update every second
            if loopCount % 30 == 0:
                print("Update Spotify Playback")
                self.user.updatePlayback()

            if loopCount % 10 == 0:
                if self.user.device == 0 or self.user.playbackState == "Not Playing":
                    print("No device playing")
                    self.canvas.Clear()
                    setText(
                        canvas=self.canvas,
                        text="no devices on",
                        position=[7, 13],
                        max_chars=16,
                        rgb=WHITE,
                    )
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)
                else:
                    # if its the first time through or song has changed
                    if (
                        not self.previousPlayback
                        or self.previousPlayback["item"]["name"]
                        != self.user.playbackState["item"]["name"]
                    ):
                        self.canvas.Clear()
                        currentSong = self.user.playbackState["item"]["name"] + "  "
                        currentArtist = (
                            self.user.playbackState["item"]["artists"][0]["name"]
                            + "   "
                        )
                        self.previousPlayback = self.user.playbackState
                        albumCover = self.user.playbackState["item"]["album"]["images"][
                            0
                        ]["url"]
                        song_duration = self.user.playbackState["item"]["duration_ms"]
                        bubblesFilled = 0
                        image = retrieve_url_image(albumCover)

                    else:
                        self.canvas.Clear()
                        song_progress = self.user.playbackState["progress_ms"]
                        bubblesFilled = int(song_progress / song_duration * 33)
                        if len(currentSong) > 11:
                            currentSong = currentSong[1:] + currentSong[0]

                        if len(currentArtist) > 11:
                            currentArtist = currentArtist[1:] + currentArtist[0]
                    #if image != None:
                        #setImage(canvas=self.canvas, image=image, dims=[24, 24], position=[2, 4])
                    setBubbles(canvas=self.canvas, bubblesFilled=bubblesFilled)
                    setText(
                        canvas=self.canvas,
                        text=currentSong,
                        posititon=[27, 6],
                        max_chars=9,
                        rgb=WHITE,
                    )
                    setText(
                        canvas=self.canvas,
                        text=currentArtist,
                        position=[27, 13],
                        max_chars=9,
                        rgb=WHITE,
                    )

                    self.canvas = self.matrix.SwapOnVSync(self.canvas)

            # updates playback every 3 seconds

            time.sleep(0.1)
            if loopCount == 150:
                loopCount = 0
            else:
                loopCount += 1

    #TODO update pages, button actions, and typing
    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()
        self.setupGPIO()
        
        self.curr_page = PageSelectionScreen(self.canvas, DASHBOARD_STATES)
        self.curr_page.init_page(self.matrix, 0)

        i = 0
        while True:
            print(f"rendering with {i}")
            self.curr_page.update_page(self.matrix, i)
            i += 1

            time.sleep(5)

    #TODO update typing
    def setupGPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(MIDDLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            LEFT_PIN, GPIO.FALLING, callback=self.buttonActions, bouncetime=200
        )
        GPIO.add_event_detect(
            MIDDLE_PIN, GPIO.FALLING, callback=self.buttonActions, bouncetime=200
        )
        GPIO.add_event_detect(
            RIGHT_PIN, GPIO.BOTH, callback=self.buttonActions, bouncetime=200
        )

    #TODO update typing
    def destroy(self):
        self.canvas.Clear()
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
        GPIO.cleanup()

    #TODO update button actions to be page specific
    def buttonActions(self, channel):
        if channel == LEFT_PIN:
            print("Left Button Pressed")
        elif channel == MIDDLE_PIN:
            print("Middle Button Pressed")
        elif channel == RIGHT_PIN:
            print("Right Button Pressed")
        else:
            print("Not sure what button was pressed")
        
        # Back button was released
        if channel == LEFT_PIN:

            if self.currMode == "Spotify":
                print("Back Pressed")
                self.user.alterPlayback("previous")
                self.user.updatePlayback()

            elif self.currMode == "Pages":
                self.selection = self.selection - 1 if self.selection != 0 else 2
                self.keepRunning = False

        # Next button was released
        elif channel == RIGHT_PIN:
            if self.currMode == "Spotify":
                print("Next Pressed")
                self.user.alterPlayback("next")
                self.user.updatePlayback()

            elif self.currMode == "Pages":
                self.selection = self.selection + 1 if self.selection != 2 else 0
                self.keepRunning = False

        # Pause button was pressed
        elif channel == MIDDLE_PIN and GPIO.input(MIDDLE_PIN) == 0:
            self.pressTime = datetime.now()

        # Pause button was released
        # elif channel == MIDDLE_PIN and GPIO.input(MIDDLE_PIN) == 1:
        #     releaseTime = datetime.now()
        #     holdTime = releaseTime - self.pressTime

        #     # button was held, opens the pages tab
        #     if holdTime >= timedelta(seconds=0.75) and self.currMode != "Pages":
        #         print("Middle Button Held")
        #         self.currMode = "Pages"
        #         self.keepRunning = False

        #     elif self.currMode == "Spotify":
        #         if self.user.playbackState["is_playing"]:
        #             self.user.alterPlayback("pause")
        #         else:
        #             self.user.alterPlayback("play")
        #         self.user.updatePlayback()
        #     elif self.currMode == "Pages":
        #         self.currMode = DASHBOARD_STATES[self.selection]
        #         self.keepRunning = False

        # ???
        else:
            print("{channel} Pressed")

if __name__ == "__main__":
    try:
        dashboard = Dashboard()
        if not dashboard.process():
            dashboard.print_help()
    except KeyboardInterrupt:
        dashboard.destroy()
