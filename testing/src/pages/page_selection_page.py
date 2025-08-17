from typing import Any, List

from pages.base_page import BasePage
from lib.components.grid import Grid 

PAGES_POS = (4, 2)
PAGES_X = 10
PAGES_SPACING = (1, 2)

REFRESH_TIME = 0  

class PageSelectionPage(BasePage):
    def __init__(self, canvas: Any, pages: List[str]) -> None:
        super().__init__(canvas)
        self.refresh_time = REFRESH_TIME

        self.pages = [" " + page for page in pages]
        self.page_selection = -1

        self._init_blank()

    def init_page(self, matrix: Any, selection: int) -> None:
        self.canvas.Clear()
        self._update_data(selection)

        self.pages_grid.update_and_render(self.canvas, self.pages)

        matrix.SwapOnVSync(self.canvas)

    def update_page(self, matrix: Any, new_selection: int) -> None:
        self._update_data(new_selection)
        self._update_display()

        matrix.SwapOnVSync(self.canvas)
    
    def _update_data(self, new_selection: int) -> None:
        if new_selection >= len(self.pages):
            print("New Selection out of bounds, setting to 0")
            new_selection = 0
        
        self.pages[self.page_selection] = self.pages[self.page_selection].replace("|", " ", 1)
        self.pages[new_selection] = self.pages[new_selection].replace(" ", "|", 1)

        self.page_selection = new_selection

    def _update_display(self) -> None:
        self.pages_grid.update_and_render(self.canvas, self.pages)

    def _init_blank(self) -> None:
        self.pages_grid = Grid(position=PAGES_POS, dims=(PAGES_X, len(self.pages)), spacing=PAGES_SPACING, font_size="s", content=[""] * len(self.pages))
    