import math
from typing import Tuple, Any

from pages.base_page import BasePage
from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay
from lib.api_users.datetime_user import DateTimeUser
from lib.helpers import get_image

IMAGE_POS = (1, 4)
CLOCK_CENTER = (11, 14)
IMAGE_SIZE = (24, 24)

GRID_SIZE = (9, 2)
TIME_GRID_POS = (27, 4)
TIME_GRID_SPACING = (1, 1)
DATE_GRID_POS = (27, 17)
DATE_GRID_SPACING = (1, 1)

FILE_PATH = "../lib/images/clock_frame.png"
MINUTE_ARM_LENGTH = 9
HOUR_ARM_LENGTH = 6

class HomePage(BasePage):
    def __init__(self, canvas: Any) -> None:
        super().__init__(canvas)
        self.user: DateTimeUser = DateTimeUser()
        self.refresh_time = 60 - self.user.seconds

        self._init_blank()

    def init_page(self, matrix: Any) -> None:
        self.canvas.Clear()
        self._update_data()

        self.time_grid.update_and_render(self.canvas, [self.user.time, ""])
        self.date_grid.update_and_render(self.canvas, [self.user.year, self.user.day_and_date])

        clock_frame_image = get_image(FILE_PATH)
        self.clock_frame_display.update_display(self.canvas, clock_frame_image)
        render_clock_arms(self.canvas, self.user.time, CLOCK_CENTER)

        matrix.SwapOnVSync(self.canvas)
    
    def update_page(self, matrix: Any) -> None:
        self._update_data()        
        self._update_display()

        matrix.SwapOnVSync(self.canvas)
            
    def _update_data(self) -> None:
        self.user.update_data()
        self.refresh_time = 60 - self.user.seconds

    def _update_display(self) -> None:
        self.time_grid.update_and_render(self.canvas, [self.user.time, ""])
        
        self.date_grid.update_and_render(self.canvas, [self.user.year, self.user.day_and_date])
        
        self.clock_frame_display.make_display(self.canvas)
        render_clock_arms(self.canvas, self.user.time, CLOCK_CENTER)

    def _init_blank(self) -> None:
        self.time_grid = Grid(position=TIME_GRID_POS, dims=GRID_SIZE, spacing=TIME_GRID_SPACING, font_size="s", content=["", ""])
        self.date_grid = Grid(position=DATE_GRID_POS, dims=GRID_SIZE, spacing=DATE_GRID_SPACING, font_size="s", content=["", ""])
        self.clock_frame_display = ImageDisplay(position=IMAGE_POS, dims=IMAGE_SIZE, image=None)

#TODO update function to a better line drawing alg
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

