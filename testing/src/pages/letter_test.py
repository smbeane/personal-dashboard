from typing import Any


from src.pages.base_page import BasePage
from lib.components.grid import Grid

REFRESH_TIME = 999

POSITION = (0, 0)
DIMS = (13, 4)

class LettersPage(BasePage):
    def __init__(self, canvas: Any, font_size: str):
        super().__init__(canvas)
        self.refresh_time = REFRESH_TIME
        
        self.font_size = font_size

        self._init_blank()

    def init_page(self, matrix: Any):
        self.canvas.Clear()
        
        self.characters_grid.initial_render(self.canvas)

    def _init_blank(self):
        row_1 = "abcdefghij"
        row_2 = "klmnopqrst"
        row_3 = "uvwxyz.()'"
        row_4 = "-/\\!$:|_?"
        
        self.characters_grid = Grid(position=POSITION, dims=DIMS, spacing=(1, 2), font_size=self.font_size, content=[row_1, row_2, row_3, row_4])

