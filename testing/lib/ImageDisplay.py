from displayFunctions import set_image
from PIL.ImageFile import ImageFile

class ImageDisplay: 
    def __init__(self, position: tuple[int, int], dims: tuple[int, int], image: ImageFile) -> None: 
        self.posiiton = position
        self.dims = dims
        self.image = image
    
    def make_display(self, canvas):
        if self.image.mode != "RGB":
            self.image = self.image.convert("RGB")

        [length_x, length_y] = self.dims
        [start_x, start_y] = self.position
        allpixels = list(self.image.getdata())

        for y in range(0, length_y):
            for x in range(0, length_x):
                color = allpixels[y * length_x + x]
                canvas.SetPixel(x + start_x, y + start_y, color[0], color[2], color[1])

    def update_display(self, canvas, image: ImageFile) -> None:
        self.image = image
        self.make_display(canvas)
    

