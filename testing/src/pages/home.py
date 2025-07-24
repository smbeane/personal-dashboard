import time as time
from datetime import datetime, timedelta

from base import BaseScreen
from lib.Grid import Grid
from lib.ImageDisplay import ImageDisplay

WHITE = [255, 255, 255]

class HomeScreen(BaseScreen):
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.dateTime = ("", "", "", 0)
        self.sleep_counter = 0
        self.page_active = False

    def updateData(self) -> tuple[str, str, str, int]:
        now = datetime.now()
    
        day_and_date = now.strftime("%a %b%d")
        year = now.strftime("     %Y")
        time = now.strftime("%I:%M %p")
        seconds = now.strftime("%S")

        return (time, day_and_date, year, int(seconds))

    def renderScreen(self):
        self.page_active = True
        self.dateTime = self.updateData()
        self.canvas.clear()

        time_grid = Grid(self.canvas, (29, 5), (9, 2), "s", [self.dateTime[0]])
        date_grid = Grid(self.canvas, (29, 18), (9, 2), "s", [self.dateTime[1], self.dateTime[2]])
        
        while self.page_active: 
            print("Updating Home Screen")
            time.sleep(self.dateTime[3])
            self.dateTime = self.updateData()

            time_grid.update_display(self.canvas, [self.dateTime[0]])
            date_grid.update_display(self.canvas, [self.dateTime[1], self.dateTime[2]])
