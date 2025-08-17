from typing import Any
from PIL import Image
import requests
from io import BytesIO

from pages.base_page import BasePage
from lib.api_users.spotify_user import SpotifyUser
from lib.components.grid import Grid
from lib.components.image_display import ImageDisplay
from lib.components.progress_bar import ProgressBar
from lib.helpers import retrieve_url_image

REFRESH_TIME = 1
WHITE = (255, 255, 255)
BLUE = (63, 81, 181)

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
        self.refresh_time = REFRESH_TIME

        self.user = SpotifyUser()
        self.update_code = 0

        self._init_blank()

    def init_page(self, matrix: Any) -> None:
        self.canvas.Clear()
        self.update_code = self._update_data()

        if self.update_code == 204:
            self._no_devices()
            matrix.SwapOnVSync(self.canvas)
            return
        
        if self.update_code == 400:

            self._error()
            matrix.SwapOnVSync(self.canvas)
            return
        
        song = self.user.parsed_playback["song"] + "  "
        artist = self.user.parsed_playback["artist"] + "  "
        progress = self.user.parsed_playback["progress"]
        cover_url = self.user.parsed_playback["album_cover_url"]


        self.names_grid.update_and_render(self.canvas, [song, artist])
        
        cover_image = retrieve_url_image(cover_url)
        self.album_display.update_display(self.canvas, cover_image)

        self.progress_bar.initial_render(self.canvas, progress)    

        matrix.SwapOnVSync(self.canvas)
        
    def update_page(self, matrix: Any, refresh_loop: int) -> None:
        if refresh_loop % 3 == 0:
            self.update_code = self._update_data()
        self._update_display(matrix)

        matrix.SwapOnVSync(self.canvas)

    def _update_data(self) -> int:
        updated = self.user.update_data()

        return updated
    
    def _update_display(self, matrix) -> None:
        if self.update_code == 0:
            self.init_page(matrix)

        if self.update_code == 400:
            self._error()
            return
        
        if self.update_code == 204:
            self._no_devices()
            return

        song = self.user.parsed_playback["song"] + "  "
        artist = self.user.parsed_playback["artist"] + "  "
        progress = self.user.parsed_playback["progress"]
        cover_url = self.user.parsed_playback["album_cover_url"]
        
        self.names_grid.update_and_render(self.canvas, [song, artist])
        self.progress_bar.update_progress(self.canvas, progress)

        if self.update_code == 202:

            cover_image = retrieve_url_image(cover_url)
            self.album_display.update_display(self.canvas, cover_image)
 
    def _no_devices(self) -> None:
        self.canvas.Clear()
        no_devices_grid = Grid(NO_DEVICES_POS, NO_DEVICES_SIZE, "s", ["no devices on"])
        no_devices_grid.initial_render(self.canvas)
    
    def _error(self) -> None:
        self.canvas.Clear()
        error_grid = Grid(NO_DEVICES_POS, NO_DEVICES_SIZE, "s", ["update errors"])
        error_grid.initial_render(self.canvas)
    
    def _init_blank(self) -> None:
        self.names_grid = Grid(NAMES_POS, NAMES_SIZE, "s", ["", ""])
        self.album_display = ImageDisplay(COVER_POS, COVER_SIZE, None)
        self.progress_bar = ProgressBar(PROGRESS_POS, PROGRESS_SIZE, WHITE, BLUE)

    def alter_playback(self, alteration: str) -> None:
        pass
