from typing import Any, Tuple
from PIL import Image
from PIL.Image import Image as Image_Type

from pages.base_screen import BaseScreen
from lib.weatherDateFunctions import getDays, getWeatherVals

from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay
from lib.components.divider import Divider


LAT = 40.4249916
LONG = -86.9063623
BLUE = [63, 81, 181]

IMAGE_POS = (0, 0)
IMAGE_SIZE = (24, 18)

DIVIDER_POS = (24, 2)
DIVIDER_LEN = 28

class Weather():
    def __init__(self, todays_weather: str, low_temps: Tuple[int], high_temps: Tuple[int]):
        self.todays_weather = todays_weather
        self.todays_low = low_temps[0]
        self.todays_high = high_temps[0]
        self.low_temps = low_temps[1:]
        self.high_temps = high_temps[1:]


class WeatherScreen(BaseScreen):
    def __init__(self, canvas: Any) -> None:
        super().__init__(canvas)
        self.page_active = False
        self.days = None
        self.weather = None
        self.imageURL = None
        
    
    def update(self, matrix: Any) -> None:
        self.page_active = True
        self.update_data()
        self.canvas.Clear()

        self.init_display()
        matrix.SwapOnVSync(self.canvas)

        while self.page_active:
            pass
        
    def update_data(self) -> None:
        todays_weather, low_temps, high_temps = getWeatherVals(LAT, LONG)
        self.weather = Weather(todays_weather, low_temps, high_temps)
        self.days = getDays()

        self.imageURL = "/home/smbeane5235/spotify/extras/icons/" + todays_weather + ".png"
        

    def init_display(self):
        weather_image = get_image(self.imageURL)
        weather_image_display = ImageDisplay(IMAGE_POS, IMAGE_SIZE, weather_image)
        weather_image_display.make_display(self.canvas)

        divider = Divider(DIVIDER_POS, DIVIDER_LEN, BLUE)
        divider.render_divider(self.canvas)

        #todays temperature grid


        #all days temperature grid



    def update_page(self):
        pass


def getDays() -> Tuple:
    return ()

def get_image(ref: str) -> Image_Type: 
    image = Image.open(ref)

    return image