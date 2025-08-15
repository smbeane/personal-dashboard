from typing import Any

REFRESH_TIME = 3

class BasePage():
    def __init__(self, canvas: Any):
        self.canvas = canvas
        self.refresh_time = REFRESH_TIME
            
    def init_page(self, matrix: Any) -> None:
        self.canvas.Clear()
        self._update_data()

        #initilize grids and images

        matrix.SwapOnVSync(self.canvas)
        
    def update_page(self, matrix: Any) -> None:        
        self._update_data()
        self._update_display()

        matrix.SwapOnVSync(self.canvas)

    def _update_data(self) -> None:
        pass

    def _update_display(self) -> None:
        pass

    