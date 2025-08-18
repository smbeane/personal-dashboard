#!/usr/bin/env python3

import time
from typing import Any

from samplebase import SampleBase
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from pages.page_selection_page import PageSelectionPage
from pages.spotify_page import SpotifyPage
from pages.letter_test import LettersPage
from lib.components.buttons import Buttons

DASHBOARD_PAGES = ["Home", "Weather", "Spotify"]
LEFT_PIN = 18
MIDDLE_PIN = 22
RIGHT_PIN = 35
WHITE = [255, 255, 255]
BLUE = [63, 81, 181]

#ELKHART
# LAT = 41.6871992
# LONG = -85.976669
#WEST LAFAYETTE
LAT = 40.4249916
LONG = -86.9063623

HOLD_CUTOFF = 0.5

class Dashboard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.canvas: Any = None
        self.buttons = Buttons(num_buttons=3, button_pins=[LEFT_PIN, MIDDLE_PIN, RIGHT_PIN], functions=[self.left_button, self.middle_button, self.right_button], hold_cutoff=HOLD_CUTOFF)
        
        self.curr_page: BasePage | None = None
        self.curr_page_name = "Home"
        self.page_selection = 0

        self.page_changed = False

    def left_button(self, held: bool) -> None:
        print("Left button pressed")
        if not self.curr_page:
            return
        
        if self.curr_page_name == "Spotify":
            self.curr_page.alter_playback("previous") #type: ignore
            return  

        if self.curr_page_name == "Page Selection":
            self.page_selection = self.page_selection - 1 if self.page_selection != 0 else len(DASHBOARD_PAGES) - 1
            return
        
        #TODO add weather page scrolling by the day
        if self.curr_page_name == "Weather":

            return   
        
    def middle_button(self, held: bool) -> None:
        print("Middle button pressed")
        if held:
            self._init_page("Page Selection")
            return
        
        if self.curr_page_name == "Spotify":
            self.curr_page.alter_playback("play/pause") #type: ignore
            return

        if self.curr_page_name == "Page Selection":
            self._init_page(DASHBOARD_PAGES[self.page_selection])

    def right_button(self, held: bool) -> None:
        print("Right button pressed")
        if not self.curr_page:
            return
        
        if self.curr_page_name == "Spotify":
            self.curr_page.alter_playback("next") #type: ignore
            return

        if self.curr_page_name == "Page Selection":
            self.page_selection = self.page_selection + 1 if self.page_selection != len(DASHBOARD_PAGES) - 1 else 0
            return

        #TODO add weather page scrolling by the day
        if self.curr_page_name == "Weather":

            return
        
    def run(self) -> None:
        self.canvas = self.matrix.CreateFrameCanvas()
        self.buttons.initial_setup()
        self._init_page(self.curr_page_name)
        
        if not self.curr_page:
            print("Page Not Initialized")
            return

        refresh_loop = 0
        while True:
            refresh_loop += 1
            print(f"{time.ctime()}: Updating Page")

            i = 0
            while i < self.curr_page.refresh_time and not self.page_changed:
                i += 0.1
                time.sleep(0.1)

            self.page_changed = False
            self._update_curr_page(refresh_loop)
    
    def _destroy(self):
        if self.canvas:
            self.canvas.Clear() 
        self.matrix.SwapOnVSync(self.canvas)
        self.buttons.cleanup()

    def _init_page(self, new_page_name: str) -> None:
        match new_page_name:
            case "Home":
                self.curr_page = HomePage(self.canvas)
                self.curr_page_name = new_page_name
                self.curr_page.init_page(self.matrix)
            case "Weather":
                self.curr_page = WeatherPage(self.canvas)
                self.curr_page_name = new_page_name
                self.curr_page.init_page(self.matrix)
            case "Page Selection":
                self.curr_page = PageSelectionPage(self.canvas, DASHBOARD_PAGES)
                self.curr_page_name = new_page_name
                self.curr_page.init_page(self.matrix, 0)
            case "Spotify":
                self.curr_page = SpotifyPage(self.canvas)
                self.curr_page_name = new_page_name
                self.curr_page.init_page(self.matrix)
            case "LettersTest":
                self.curr_page = LettersPage(self.canvas, "s")
                self.curr_page_name = new_page_name
                self.curr_page.init_page(self.matrix)
            case _:
                self.curr_page = HomePage(self.canvas)
                self.curr_page_name = new_page_name
                self.curr_page.init_page(self.matrix)

        self.page_changed = True

    def _update_curr_page(self, refresh_loop: int) -> None:
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




if __name__ == "__main__":
    dashboard: Dashboard | None = None    
    
    try:
        dashboard = Dashboard()
        if not dashboard.process():
            dashboard.print_help() #type: ignore
    finally:
        if dashboard:
            dashboard._destroy()
