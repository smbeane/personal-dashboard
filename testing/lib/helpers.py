import requests
from datetime import datetime
from typing import Any, Tuple, List
from PIL import Image
from io import BytesIO

from lib.letters import small_font, medium_font, large_font

WHITE = (255, 255, 255)
BLUE = (63, 81, 181)

SMALL = (3, 5)
MEDIUM = (4, 6)
LARGE = (5, 7)

def set_character(canvas: Any, size: str, character: str, position: Tuple[int, int], rgb: Tuple[int, int, int] = WHITE):
    character = character.lower()   

    match size:
        case "s":
            font = small_font
            width, height = SMALL
        case "m":
            font = medium_font
            width, height = MEDIUM
        case "l":
            font = large_font
            width, height = LARGE
        case _:
            font = small_font
            width, height = SMALL
    
    if character not in font:
        character = "?"

    char_int = font[character]
    start_x, start_y = position
    r_on, g_on, b_on = rgb
        
    for row in range(height):
        for col in range(width):
            index = (height - 1 - row) * width + (width - 1 - col)
            r, g, b = (r_on, g_on, b_on) if char_int & 1 << index else (0, 0, 0)
            
            canvas.SetPixel(start_x + col, start_y + row, r, b, g)

def retrieve_url_image(album_cover: str) -> Image.Image | None:
    response = requests.get(album_cover)

    if response.ok:
        image = Image.open(BytesIO(response.content))
        image = image.resize((24, 24))

        return image

    else:
        print("Failed to download image:", response.status_code)
        return None
    
def get_image(ref: str) -> Image.Image: 
    image = Image.open(ref)

    return image

def get_days() -> List[str]:
    days_all = ["mon","tue","wed","thu","fri","sat","sun"]
    today_index = datetime.now().weekday()
    
    return [days_all[(today_index + i) % 7] for i in range(5)]