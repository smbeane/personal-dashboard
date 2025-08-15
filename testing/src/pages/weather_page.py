from typing import Any, List
from PIL import Image
from datetime import datetime

from pages.base_page import BasePage
from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay
from lib.components.divider import Divider
from lib.api_users.open_meteo_user import OpenMeteoUser

REFRESH_TIME = 30 * 60

LAT = 40.4249916
LONG = -86.9063623
JOINING_CHAR = "|"

IMAGE_DIR = "/home/smbeane5235/spotify/extras/icons/"
IMAGE_POS = (0, 0)
IMAGE_SIZE = (24, 18)

BLUE = [63, 81, 181]
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
        
        self.weather_image_display: ImageDisplay = None
        self.todays_grid: Grid = None
        self.week_grid: Grid = None

    def init_page(self, matrix: Any) -> None:
        self.canvas.Clear()
        self._update_data()
        
        weather_image = get_image(self.image_url)
        self.weather_image_display = ImageDisplay(IMAGE_POS, IMAGE_SIZE, weather_image)
        self.weather_image_display.make_display(self.canvas)

        divider = Divider(DIVIDER_POS, DIVIDER_LEN, BLUE)
        divider.render_divider(self.canvas)

        temps = join_strs(self.user.todays_low, self.user.todays_high)
        self.todays_grid = Grid(TODAYS_POS, TODAYS_SIZE, "s", ["today", temps])
        self.todays_grid.initial_render(self.canvas)

        grid_text = self._get_grid_text()
        self.week_grid = Grid(TEMPS_POS, TEMPS_SIZE, "s", grid_text)
        self.week_grid.initial_render(self.canvas)

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
        weather_image = get_image(self.image_url)
        self.weather_image_display.update_display(weather_image)

        self.todays_grid.update_and_render(self.canvas, ["today", join_strs(self.user.todays_low, self.user.todays_high)])

        grid_text = self._get_grid_text()
        self.week_grid.update_and_render(self.canvas, grid_text)

    def _get_grid_text(self) -> List[str]:
        grid_text = []
        
        for i in range(0, 4):
            joined_temps = join_strs(self.user.low_temps[i], self.user.high_temps[i])
            day_and_temps = " ".join([self.days[i], joined_temps])
            grid_text.append(day_and_temps)

        return grid_text

def join_strs(first_str: int | str, second_str: int | str, joining_char: str = JOINING_CHAR) -> str:
    first_str = str(first_str).zfill(2)
    second_str = str(second_str).zfill(2)
    return f"{first_str}{joining_char}{second_str}"

def get_days() -> List[str]:
    days_all = ["mon","tue","wed","thu","fri","sat","sun"]
    today_index = datetime.now().weekday()
    
    return [days_all[(today_index + i) % 7] for i in range(5)]

def get_image(ref: str) -> Image.Image: 
    image = Image.open(ref)

    return image

