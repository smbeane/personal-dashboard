from typing import Any, List
from PIL import Image
from datetime import datetime

from pages.base_page import BasePage
from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay
from lib.components.divider import Divider
from lib.api_users.open_meteo_user import OpenMeteoUser

from lib.helpers import get_image, get_days, BLUE

REFRESH_TIME = 30 * 60

LAT = 40.4249916
LONG = -86.9063623
JOINING_CHAR = "|"

IMAGE_DIR = "/home/smbeane5235/spotify/extras/icons/"
IMAGE_POS = (0, 0)
IMAGE_SIZE = (24, 18)

DIVIDER_POS = (24, 2)
DIVIDER_LEN = 28

TODAYS_POS = (2, 19)
TODAYS_SIZE = (5, 2)
TEMPS_POS = (27, 4)
TEMPS_SIZE = (9, 4)

class WeatherPage(BasePage):
    def __init__(self, canvas: Any) -> None:
        super().__init__(canvas)
        self.refresh_time = REFRESH_TIME

        self.user = OpenMeteoUser(LAT, LONG)
        self.image_url = None
        self.weather_changed = False
        self.days = []
        
        self._init_blank()

    def init_page(self, matrix: Any) -> None:
        self.canvas.Clear()
        self._update_data()
        
        if self.image_url:
            weather_image = get_image(self.image_url)
            self.weather_image_display.update_display(self.canvas, weather_image)

        self.divider.render_divider(self.canvas)

        temps = join_strs(self.user.todays_low, self.user.todays_high)
        self.todays_grid.update_and_render(self.canvas, ["today", temps])

        grid_text = self._get_grid_text()
        self.week_grid.update_and_render(self.canvas, grid_text)

        matrix.SwapOnVSync(self.canvas)
    
    def update_page(self, matrix: Any) -> None:
        self._update_data()
        self._update_display()

        matrix.SwapOnVSync(self.canvas)

    def _update_data(self) -> None:
        self.user.update_data()
        self.days = get_days()

        self.image_url = IMAGE_DIR + self.user.todays_weather + ".png"
        

    def _update_display(self) -> None:
        if self.image_url:
            weather_image = get_image(self.image_url)
            self.weather_image_display.update_display(self.canvas, weather_image)
        
        self.todays_grid.update_and_render(self.canvas, ["today", join_strs(self.user.todays_low, self.user.todays_high)])

        grid_text = self._get_grid_text()
        self.week_grid.update_and_render(self.canvas, grid_text)

    def _get_grid_text(self) -> List[str]:
        grid_text = []
        
        if self.user.low_temps and self.user.high_temps:
            for i in range(0, 4):
                joined_temps = join_strs(self.user.low_temps[i], self.user.high_temps[i])
                day_and_temps = " ".join([self.days[i], joined_temps])
                grid_text.append(day_and_temps)

        return grid_text
    
    def _init_blank(self) -> None:
        self.weather_image_display = ImageDisplay(IMAGE_POS, IMAGE_SIZE, None)
        self.todays_grid = Grid(TODAYS_POS, TODAYS_SIZE, "s", ["", ""])

        self.divider = Divider(DIVIDER_POS, DIVIDER_LEN, BLUE)
        self.week_grid = Grid(TEMPS_POS, TEMPS_SIZE, "s", ["", "", "", ""])

def join_strs(first_str: int | str | None, second_str: int | str | None, joining_char: str = JOINING_CHAR) -> str:
    if not first_str:
        return str(second_str)
    
    if not second_str:
        return str(first_str)
    
    first_str = str(first_str).zfill(2)
    second_str = str(second_str).zfill(2)
    return f"{first_str}{joining_char}{second_str}"
