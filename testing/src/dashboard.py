from samplebase import SampleBase
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from PIL import Image

from pages.home import HomeScreen

from lib.SpotifyClass import SpotifyUser
from lib.displayFunctions import (
    retrieveURLImage,
    setImage,
    setBubbles,
    setText,
    setDivider,
)
from lib.weatherDateFunctions import getDays, getTimeAndDate, getWeatherVals

DASHBOARD_STATES = ["Home", "Weather", "Spotify"]
BACK_PIN = 18
PAUSE_PIN = 22
NEXT_PIN = 35
WHITE = [255, 255, 255]
BLUE = [63, 81, 181]

LAT = 40.4249916
LONG = -86.9063623


class Dashboard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.canvas = self.matrix.CreateFrameCanvas()
        self.home_screen = HomeScreen(self.canvas)
        self.currMode = "Home"
        self.lastMode = "Home"
        self.user = None
        self.pressTime = 0
        self.previousPlayback = {}
        self.selection = -1
        self.keepRunning = True
        self.canvas = None

    def homeScreen(self):
        self.home_screen.render_screen()

    def weatherScreen(self):
        while self.keepRunning:
            self.canvas.Clear()
            todays_weather, low_temps, high_temps = getWeatherVals(LAT, LONG)
            days = getDays()
            image = Image.open(
                "/home/smbeane5235/spotify/extras/icons/" + todays_weather + ".png"
            )

            setImage(canvas=self.canvas, image=image, dims=[24, 18], position=[0, 0])
            setDivider(canvas=self.canvas, position=[24, 2], length=28, rgb=BLUE)

            temps = "|".join([str(low_temps[0]).zfill(2), str(high_temps[0]).zfill(2)])
            setText(
                canvas=self.canvas,
                text="today",
                position=[2, 19],
                max_chars=5,
                rgb=WHITE,
            )
            setText(
                canvas=self.canvas, text=temps, position=[2, 25], max_chars=5, rgb=WHITE
            )

            for i in range(1, 5):
                low_high = "|".join(
                    [str(low_temps[i]).zfill(2), str(high_temps[i]).zfill(2)]
                )

                full_text = " ".join([days[i], low_high])
                pos = [27, 3 + (i - 1) * 7]

                setText(
                    canvas=self.canvas,
                    text=full_text,
                    position=pos,
                    max_chars=9,
                    rgb=WHITE,
                )

            self.canvas = self.matrix.SwapOnVSync(self.canvas)

            sleepCounter = 0
            while self.keepRunning and sleepCounter < 30 * 60 * 10:
                time.sleep(0.1)
                sleepCounter += 1

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
                        image = retrieveURLImage(albumCover)

                    else:
                        self.canvas.Clear()
                        song_progress = self.user.playbackState["progress_ms"]
                        bubblesFilled = int(song_progress / song_duration * 33)
                        if len(currentSong) > 11:
                            currentSong = currentSong[1:] + currentSong[0]

                        if len(currentArtist) > 11:
                            currentArtist = currentArtist[1:] + currentArtist[0]
                    if image != None:
                        setImage(
                            canvas=self.canvas, image=image, dims=[24, 24], position=[2, 4]
                        )
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

    def pagesScreen(self):
        while self.keepRunning:
            self.canvas.Clear()

            for index, state in enumerate(DASHBOARD_STATES):
                position = [4, 2 + 7 * index]
                setText(
                    canvas=self.canvas,
                    text=state,
                    position=position,
                    max_chars=10,
                    rgb=WHITE,
                )

            if self.selection != -1:
                position = [1, 2 + 7 * self.selection]
                setText(
                    canvas=self.canvas,
                    text="|",
                    position=position,
                    max_chars=1,
                    rgb=BLUE,
                )

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

                setText(canvas=self.canvas, text="No clue", position=[0, 0], rgb=WHITE)
                self.canvas = self.matrix.SwapOnVSync(self.canvas)

                while self.keepRunning:
                    time.sleep(0.1)

            self.keepRunning = True

    def setupGPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PAUSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            BACK_PIN, GPIO.FALLING, callback=self.buttonActions, bouncetime=200
        )
        GPIO.add_event_detect(
            NEXT_PIN, GPIO.FALLING, callback=self.buttonActions, bouncetime=200
        )
        GPIO.add_event_detect(
            PAUSE_PIN, GPIO.BOTH, callback=self.buttonActions, bouncetime=200
        )

    def destroy(self):
        self.canvas.Clear()
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
        GPIO.cleanup()

    def buttonActions(self, channel):
        # Back button was released
        if channel == BACK_PIN:

            if self.currMode == "Spotify":
                print("Back Pressed")
                self.user.alterPlayback("previous")
                self.user.updatePlayback()

            elif self.currMode == "Pages":
                self.selection = self.selection - 1 if self.selection != 0 else 2
                self.keepRunning = False

        # Next button was released
        elif channel == NEXT_PIN:
            if self.currMode == "Spotify":
                print("Next Pressed")
                self.user.alterPlayback("next")
                self.user.updatePlayback()

            elif self.currMode == "Pages":
                self.selection = self.selection + 1 if self.selection != 2 else 0
                self.keepRunning = False

        # Pause button was pressed
        elif channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 0:
            self.pressTime = datetime.now()

        # Pause button was released
        elif channel == PAUSE_PIN and GPIO.input(PAUSE_PIN) == 1:
            releaseTime = datetime.now()
            holdTime = releaseTime - self.pressTime

            # button was held, opens the pages tab
            if holdTime >= timedelta(seconds=0.75) and self.currMode != "Pages":
                self.currMode = "Pages"
                self.keepRunning = False

            elif self.currMode == "Spotify":
                if self.user.playbackState["is_playing"]:
                    self.user.alterPlayback("pause")
                else:
                    self.user.alterPlayback("play")
                self.user.updatePlayback()
            elif self.currMode == "Pages":
                self.currMode = DASHBOARD_STATES[self.selection]
                self.keepRunning = False

        # ???
        else:
            print("??? Pressed")


if __name__ == "__main__":
    try:
        dashboard = Dashboard()
        if not dashboard.process():
            dashboard.print_help()
    except KeyboardInterrupt:
        dashboard.destroy()
