from typing import Tuple, Any, List

WHITE = (255, 255, 255)

class Divider:
    def __init__(self, position: Tuple[int, int], length: int, color: Tuple[int, int, int] = WHITE) -> None:
        self.x, self.y = position
        self.length = length
        self.color = color

    def render_divider(self, canvas: Any):
        [r, g, b] = self.color

        for y in range(self.y, self.y + self.length):
            canvas.SetPixel(self.x, y, r, b, g)
