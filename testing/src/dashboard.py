import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

from samplebase import SampleBase
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from pages.page_selection_page import PageSelectionPage
from pages.spotify_page import SpotifyPage


DASHBOARD_PAGES = ["Home", "Weather", "Spotify"]
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
        self.curr_page: BasePage | None = None
        self.curr_page_name = "Spotify"
        self.page_selection = 0

        self.lastMode = "Home"
        self.pressTime = 0
        self.keepRunning = True

    #TODO update pages, button actions, and typing
    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()
        self.setupGPIO()
        self.curr_page = SpotifyPage(self.canvas)
        self.curr_page_name = "Spotify" 
        self.curr_page.init_page(self.matrix)
        
        refresh_loop = 0
        while True:
            refresh_loop += 1
            print(f"{time.ctime()}: Updating Page")
            self.update_curr_page(refresh_loop)
            time.sleep(self.curr_page.refresh_time)

    def update_curr_page(self, refresh_loop: int) -> None:
        if not self.curr_page:
            return
        
        if self.curr_page_name == "Home":
            self.curr_page.update_page(self.matrix)
            return
        
        if self.curr_page_name == "Page Selection":
            self.curr_page.update_page(self.matrix, self.page_selection)
            return
            
        if self.curr_page_name == "Weather":
            self.curr_page.update_page(self.matrix)
            return
        
        if self.curr_page_name == "Spotify":
            self.curr_page.update_page(self.matrix, refresh_loop)
            return

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
        if not self.curr_page:
            return
        
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

            if self.curr_page_name == "Spotify":
                print("Previous Song")
                self.curr_page.alter_playback("previous") #type: ignore
                return

            if self.curr_page_name == "Pages":
                self.page_selection = self.page_selection - 1 if self.selection != 0 else len(DASHBOARD_PAGES) - 1
                self.curr_page.update_page(self.matrix, self.page_selection)
                return
            
            #TODO add weather page scrolling by the day
            if self.curr_page_name == "Weather":
                print("This will be where people can change the weather")
                return    
        
        if channel == MIDDLE_PIN:
            if GPIO.input(MIDDLE_PIN) == GPIO.LOW: #Button was pressed
                print("Middle button was pressed")
            else: 
                print("Middle button was released")
        
        # Next button was released
        if channel == RIGHT_PIN:
            if self.curr_page_name == "Spotify":
                print("Previous Song")
                self.curr_page.alter_playback("next") #type: ignore
                return

            elif self.curr_page_name == "Pages":
                self.selection = self.selection + 1 if self.selection != len(DASHBOARD_PAGES) - 1 else 0
                self.curr_page.update_page(self.matrix, self.page_selection)

        # elif channel == MIDDLE_PIN and GPIO.input(MIDDLE_PIN) == 0:
        #     self.pressTime = datetime.now()
        #
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
    dashboard: Dashboard | None = None    
    
    try:
        dashboard = Dashboard()
        if not dashboard.process():
            dashboard.print_help() #type: ignore
    except KeyboardInterrupt:
        if dashboard:
            dashboard.destroy()
