import requests
from PIL import Image
from PIL.ImageFile import ImageFile
from lib.letters import font

from io import BytesIO


def retrieve_url_image(albumCover: str) -> ImageFile:
    response = requests.get(albumCover)

    if response.ok:
        image = Image.open(BytesIO(response.content))
        image = image.resize((24, 24))

        return image

    else:
        print("Failed to download image:", response.status_code)
        return None

def set_character(canvas, character: str, position: tuple[int, int], rgb: tuple[int, int, int]) -> None:
    char_arr = font[character]
    start_x, start_y = position
    r_on, g_on, b_on = rgb

    for y in range(5):
        for x in range(3):
            if char_arr[y][x] == 1:
                r,g,b, = r_on, g_on, b_on,
            else:
                r, g, b = 0, 0, 0
            canvas.SetPixel(start_x + x, start_y + y, r, b, g)


# fix method, change it so that the bubble outline is permanent and the only thing that gets
# updated is the progress bar
def setBubbles(canvas, bubblesFilled):
    bubbleCount = 0

    for x in range(27, 62):
        canvas.SetPixel(x, 21, 255, 255, 255)
        canvas.SetPixel(x, 25, 255, 255, 255)

        if x == 0 or x == 34:
            canvas.SetPixel(x, 22, 255, 255, 255)
            canvas.SetPixel(x, 23, 255, 255, 255)
            canvas.SetPixel(x, 24, 255, 255, 255)
        elif bubbleCount < bubblesFilled:
            canvas.SetPixel(x, 22, 255, 255, 255)
            canvas.SetPixel(x, 23, 255, 255, 255)
            canvas.SetPixel(x, 24, 255, 255, 255)
            bubbleCount += 1
        else:
            canvas.SetPixel(x, 22, 0, 0, 0)
            canvas.SetPixel(x, 23, 0, 0, 0)
            canvas.SetPixel(x, 24, 0, 0, 0)

def setText(canvas, text, position, max_chars, rgb):
    [start_x, start_y] = position
    char_count = 0
    text = text.lower()

    for char in text:
        if char not in font:
            char = " "
        if char_count >= max_chars:
            break
        set_character(canvas, char, (start_x + char_count * 4, start_y), rgb)
        char_count += 1
