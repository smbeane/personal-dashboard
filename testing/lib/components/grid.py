from lib.letters import font
from typing import Tuple, Any, List
WHITE = (255, 255, 255)

class Grid:
    def __init__(self, position: Tuple[int, int], dims: Tuple[int, int], grid_size: str, content: List[str], color: Tuple[int, int, int] = WHITE) -> None:
        self.x, self.y = position
        self.x_len, self.y_len = dims
        self.grid_size = grid_size #will allow for text to be 3x5, 5x7, or larger?
        self.color = color

        self.full_content = content #what should go on the display, used for situations such as if a name is too long to actually fit on the display
        self.display_content = [] #content currently on the display
        self.offscreen_content = self.initialize_offscreen_content(content) #content on the offscreen canvas

    def initialize_offscreen_content(self, full_content: List[str]) -> List[List[str]]:
        offscreen_content = []
        
        for line in full_content[:self.y_len]: 
            line_arr = list(line[:self.x_len])
            offscreen_content.append(line_arr)

        return offscreen_content

    def render_offscreen(self, canvas): 
        for y_offset, line in enumerate(self.offscreen_content):
            for x_offset, character in enumerate(line):
                x_pos = self.x + x_offset * 4
                y_pos = self.y + y_offset * 6 
                set_character(canvas, character, (x_pos, y_pos), self.color)
       
        self.swap_contents()
    
    def update_offscreen_content(self, updated_content: List[str]) -> List[Tuple[int, int]]:
        updated_cells = []

        if self.offscreen_content == []:
            self.offscreen_content = self.initialize_offscreen_content(updated_content)
            return [(-1, -1)]
        
        for y_index in range(self.y_len):
            old_line = self.offscreen_content[y_index]
            new_line = list(updated_content[y_index][:self.x_len])

            if new_line == old_line:
                continue

            for x_index, (old_char, new_char) in enumerate(zip(old_line, new_line)):
                if old_char != new_char:
                    updated_cells.append((x_index, y_index))
                    self.offscreen_content[y_index][x_index] = new_char
        
        return updated_cells
    
    def update_offscreen(self, canvas: Any, updated_content: List[str]) -> None:
        updated_cells = self.update_offscreen_content(updated_content)

        if len(updated_cells) == 0:
            return
        
        if(updated_cells[0] == (-1, -1)):
            self.render_offscreen(canvas)
            return

        for x, y in updated_cells:
            character = self.offscreen_content[y][x]
            position = (self.x + x * 4, self.y + y * 6)

            set_character(canvas, character, position, self.color)
        
        self.swap_contents()
        self.content = updated_content

    #TODO
    def scroll_offscreen(self, canvas: Any) -> None:
        pass

    def swap_contents(self) -> None:
        curr_content = self.display_content
        self.display_content = self.offscreen_content
        self.offscreen_content = curr_content

def set_character(canvas: Any, character: str, position: Tuple[int, int], rgb: Tuple[int, int, int] = WHITE) -> None:
    character = character.lower()
    if character not in font:
            character = "?"

    char_arr = font[character]
    start_x, start_y = position
    r_on, g_on, b_on = rgb

    for y in range(5):
        for x in range(3):
            r, g, b = (r_on, g_on, b_on) if char_arr[y][x] == 1 else (0, 0, 0)
            
            canvas.SetPixel(start_x + x, start_y + y, r, b, g)
