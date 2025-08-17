import requests
from datetime import datetime
from typing import Any, Tuple, List
from PIL import Image
from io import BytesIO

from lib.letters import small_font, medium_font, large_font

WHITE = (255, 255, 255)
BLUE = (63, 81, 181)

def set_character(canvas: Any, size: str, character: str, position: Tuple[int, int], rgb: Tuple[int, int, int] = WHITE):
    character = character.lower()   

    match size:
        case "s":
            font = small_font
            width = 3
            height = 5
        case "m":
            font = medium_font
            width = 4
            height = 6
        case "l":
            font = large_font
            width = 5
            height = 7

        case _:
            font = small_font
            width = 3
            height = 5
    
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