from PIL.Image import Image

BLACK = (0, 0, 0)

class ImageDisplay: 
    def __init__(self, position: tuple[int, int], dims: tuple[int, int], image: Image) -> None: 
        self.position = position
        self.dims = dims
        self.image = image
    
    def make_display(self, canvas):
        [length_x, length_y] = self.dims
        [start_x, start_y] = self.position
        allpixels = list(self.image.getdata())

        for y in range(0, length_y):
            for x in range(0, length_x):
                color = allpixels[y * length_x + x]
                canvas.SetPixel(x + start_x, y + start_y, color[0], color[2], color[1])

        return canvas

    def update_display(self, canvas, image: Image) -> None:
        self.image = image
        self.make_display(canvas)
    

