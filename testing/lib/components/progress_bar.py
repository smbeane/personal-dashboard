from typing import Tuple, Any

WHITE = (255, 255, 255)

class ProgressBar():
    def __init__(self, position: Tuple[int, int], dims: Tuple[int, int], border_color: Tuple[int, int, int] = WHITE, bar_color: Tuple[int, int, int] = WHITE):
        self.x_pos, self.y_pos = position
        self.x_len, self.y_len = dims
        self.border_color = border_color
        self.bar_color = bar_color
        self.prev_cols_filled = 0

    def initial_render(self, canvas: Any, progress: float) -> None:
        self._render_border(canvas)
        self._render_progress(canvas, progress)

    def update_progress(self, canvas: Any, progress: float) -> None:
        new_cols_filled = int(progress * self.x_len)
        if self.prev_cols_filled > new_cols_filled:
            self._clear_progress(canvas)
            self.prev_cols_filled = 0

        self._render_progress(canvas, progress)

    def _render_border(self, canvas) -> None:
        r, g, b = self.border_color
        
        for x in range(self.x_pos, self.x_pos + self.x_len + 1):
            canvas.SetPixel(x, self.y_pos, r, b, g)
            canvas.SetPixel(x, self.y_pos + self.y_len, r, b, g)

            if x == self.x_pos or x == self.x_pos + self.x_len:
                for y in range(self.y_pos, self.y_pos + self.y_len + 1):
                    canvas.SetPixel(x, y, r, b, g)

    def _render_progress(self, canvas: Any, progress: float) -> None:
        r, g, b = self.bar_color
        cols_filled = int(progress * self.x_len)

        for x in range(self.x_pos + 1 + self.prev_cols_filled, self.x_pos + 1 + cols_filled):
            for y in range(self.y_pos + 1, self.y_pos + self.y_len):
                canvas.SetPixel(x, y, r, b, g)

        self.prev_cols_filled = cols_filled

    def _clear_progress(self, canvas) -> None:
        for x in range(self.x_pos + 1, self.x_pos + self.x_len):
            for y in range(self.y_pos + 1, self.y_pos + self.y_len):
                canvas.SetPixel(x, y, 0, 0, 0)
