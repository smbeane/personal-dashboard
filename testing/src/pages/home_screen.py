import time
from datetime import datetime
from PIL import Image
from PIL.Image import Image as Image_Type
import math
from typing import Tuple, Any

from pages.base_screen import BaseScreen
from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay

WHITE = [255, 255, 255]
IMAGE_POS = (1, 4)
CLOCK_CENTER = (11, 14)
IMAGE_SIZE = (24, 24)

GRID_SIZE = (9, 2)
TIME_GRID_POS = (28, 4)
DATE_GRID_POS = (28, 17)

FILE_PATH = "../lib/images/clock_frame.png"
MINUTE_ARM_LENGTH = 9
HOUR_ARM_LENGTH = 6

class DateAndTime():
    def __init__(self, time: str, day_and_date: str, year: str, seconds: int) -> None:
        self.time = time
        self.day_and_date = day_and_date
        self.year = year
        self.seconds = seconds

class HomeScreen(BaseScreen):
    def __init__(self, canvas: Any) -> None:
        super().__init__(canvas)
        self.page_active = False
        self.dateTime = None
        self.sleep_counter = 0

    def update(self, matrix: Any) -> None:
        self.page_active = True
        self.update_data()
        self.canvas.Clear()

        time_grid, date_grid, clock_frame = self.init_display()

        while self.page_active:
            matrix.SwapOnVSync(self.canvas) 
            time.sleep(int(60 - self.dateTime.seconds) + 1)
            self.update_data()

            self.update_display(time_grid, date_grid, clock_frame)
            
    def update_data(self) -> None:
        now = datetime.now()
    
        day_and_date = now.strftime("%a %b%d")
        year = now.strftime("     %Y")
        curr_time = now.strftime(" %I:%M%p ")
        seconds = now.second

        self.dateTime = DateAndTime(curr_time, day_and_date, year, seconds)

    def init_display(self) -> Tuple[Grid, Grid, ImageDisplay]:
        time_grid = Grid(TIME_GRID_POS, GRID_SIZE, "s", [self.dateTime.time, ""])
        time_grid.render_offscreen(self.canvas)
        
        date_grid = Grid(DATE_GRID_POS, GRID_SIZE, "s", [self.dateTime.year, self.dateTime.day_and_date])
        date_grid.render_offscreen(self.canvas)

        clock_frame_image = get_image(FILE_PATH)
        clock_frame_display = ImageDisplay(IMAGE_POS, IMAGE_SIZE, clock_frame_image)
        clock_frame_display.make_display(self.canvas)
        render_clock_arms(self.canvas, self.dateTime.time, CLOCK_CENTER)


        return (time_grid, date_grid, clock_frame_display)
    
    def update_display(self, time_grid: Grid, date_grid: Grid, clock_frame: ImageDisplay) -> None:
        time_grid.update_offscreen(self.canvas, [self.dateTime.time, ""])
        date_grid.update_offscreen(self.canvas, [self.dateTime.year, self.dateTime.day_and_date])
        clock_frame.make_display(self.canvas)
        render_clock_arms(self.canvas, self.dateTime.time, CLOCK_CENTER)


def get_image(ref: str) -> Image_Type: 
    image = Image.open(ref)

    return image

#needs updating
def render_clock_arms(canvas: Any, time: str, start_pos: Tuple[int, int]) -> None:
    start_x, start_y = start_pos
    time = time.strip().upper().replace("AM", "").replace("PM", "")
    hr_str, minute_str = time.split(":")
    hr = int(hr_str)
    minute = int(minute_str)

    minute_angle = (minute / 60) * 2 * math.pi
    hour_angle = ((hr % 12) / 12 + minute / 720) * 2 * math.pi

    minute_dx = math.cos(minute_angle - math.pi / 2)
    minute_dy = math.sin(minute_angle - math.pi / 2)

    for i in range(1, MINUTE_ARM_LENGTH):
        minute_x = start_x
        minute_y = start_y
        match minute:
            case 0 | 1 | 2 | 3 | 4:
                minute_x += 2
            case 5 | 6 | 7 | 8 | 9:
                minute_x += 3
            case 10 | 11 | 12 | 13 | 14:
                minute_x += 3
                minute_y += 1
            case 15| 16 | 17 | 18 | 19:
                minute_x += 3
                minute_y += 2
            case 20 | 21 | 22 | 23 | 24:
                minute_x += 3
                minute_y += 3
            case 25 | 26 | 27 | 28 | 29:
                minute_x += 2
                minute_y += 3
            case 30 | 31 | 32 | 33 | 34:
                minute_x += 1
                minute_y += 3
            case 35 | 36 | 37 | 38 | 39:
                minute_y += 3
            case 40 | 41 | 42 | 43 | 44:
                minute_y += 2
            case 45 | 46 | 47 | 48 | 49:
                minute_y += 1
            case 55 | 56 | 57 | 58 | 59:
                minute_x += 1
        
        x = round(minute_dx * i)
        y = round(minute_dy * i)
        canvas.SetPixel(minute_x + x, minute_y + y, 255, 0, 111)

    hour_dx = math.cos(hour_angle - math.pi / 2)
    hour_dy = math.sin(hour_angle - math.pi / 2)

    for i in range(1, HOUR_ARM_LENGTH):
        hour_x = start_x
        hour_y = start_y

        match hr:
            case 12:
                hour_x += 2
            case 1:
                hour_x += 3
            case 2:
                hour_x += 3
                hour_y += 1
            case 3:
                hour_x += 3
                hour_y += 2
            case 4:
                hour_x += 3
                hour_y += 3
            case 5:
                hour_x += 2
                hour_y += 3
            case 6:
                hour_x += 1
                hour_y += 3
            case 7:
                hour_y += 3
            case 8:
                hour_y += 2
            case 9:
                hour_y += 1
            case 11:
                hour_x += 1


        x = round(hour_dx * i)
        y = round(hour_dy * i)
        canvas.SetPixel(hour_x + x, hour_y + y, 255, 0, 111)

