from typing import Any
from PIL import Image
import requests
from io import BytesIO

from pages.base_page import BasePage
from lib.api_users.spotify_user import SpotifyUser
from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay
from lib.components.progress_bar import ProgressBar

COVER_POS = (2, 4)
COVER_SIZE = (24, 24)

NAMES_POS = (27, 6)
NAMES_SIZE = (9, 2)

PROGRESS_POS = (27, 21)
PROGRESS_SIZE = (34, 5)

NO_DEVICES_POS = (7, 13)
NO_DEVICES_SIZE = (16, 1)



class SpotifyPage(BasePage):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.user = SpotifyUser()

        self.album_display: ImageDisplay = None
        self.names_grid: Grid = None
        self.progress_bar: ProgressBar = None

    def init_page(self, matrix: Any) -> None:
        self.canvas.Clear()
        self._update_data()

        if self.user.raw_playback == "No device playing":
            self._no_devices()
            matrix.SwapOnVSync(self.canvas)
            return
        
        if self.user.raw_playback == "Error updating playback":
            self._error()
            matrix.SwapOnVSync(self.canvas)
            return
        
        song = self.user.parsed_playback["song"]
        artist = self.user.parsed_playback["artist"]

        self.names_grid = Grid(NAMES_POS, NAMES_SIZE, "s", [song, artist])
        self.names_grid.initial_render(self.canvas)

        cover_image = retrieve_url_image(self.user.parsed_playback["album_cover_url"])
        self.album_display = ImageDisplay(COVER_POS, COVER_SIZE, cover_image)
        self.album_display.make_display(self.canvas)

        self.progress_bar = ProgressBar(PROGRESS_POS, PROGRESS_SIZE)
        self.progress_bar.initial_render(self.canvas, self.user.parsed_playback["progress"])

        matrix.SwapOnVSync(self.canvas)
        
    def update_page(self, matrix: Any) -> None:        
        self._update_data()
        self._update_display()

        matrix.SwapOnVSync(self.canvas)

    def _update_data(self) -> bool:
        updated = self.user.update_data()


        return updated
    def _update_display(self) -> None:
        pass

    def _no_devices(self) -> None:
        no_devices_grid = Grid(NO_DEVICES_POS, NO_DEVICES_SIZE, "s", ["no devices on"])
        no_devices_grid.initial_render(self.canvas)
    
    def _error(self) -> None:
        error_grid = Grid(NO_DEVICES_POS, NO_DEVICES_SIZE, "s", ["update errors"])
        error_grid.initial_render(self.canvas)
    

def retrieve_url_image(albumCover: str) -> Image.Image:
    response = requests.get(albumCover)

    if response.ok:
        image = Image.open(BytesIO(response.content))
        image = image.resize((24, 24))

        return image

    else:
        print("Failed to download image:", response.status_code)
        return None
