from letters import font

WHITE = (255, 255, 255)

class Grid:
    def __init__(self, canvas, position: tuple[int, int], dims: tuple[int, int], grid_size: str, content: list[str], color: tuple[int, int, int] = WHITE) -> None:
        self.x, self.y = position
        self.x_len, self.y_len = dims
        self.grid_size = grid_size
        self.full_content = content
        self.display_content = self.fill_display_content(content)
        self.color = color

        self.fill_display(canvas)

    def fill_display_content(self, full_content: list[str]) -> list[list[str]]:
        display_content = []
        for line in full_content[:self.y_len]: 
            line_arr = list(line[:self.x_len])
            display_content.append(line_arr)

        return display_content

    def update_display_content(self, updated_content: list[str]) -> list[tuple[int, int]]:
        updated_cells = []
        for y_index in range(self.y_len):
            old_line = self.display_content[y_index]
            new_line = list(updated_content[y_index][:self.x_len])

            if new_line == old_line:
                continue

            for x_index, (old_char, new_char) in enumerate(zip(old_line, new_line)):
                if old_char != new_char:
                    updated_cells.append((x_index, y_index))
                    self.display_content[y_index][x_index] = new_char
        
        return updated_cells
    
    def fill_display(self, canvas) -> None: 
        for y_offset, line in enumerate(self.display_content[:self.y_len]):
            for x_offset, character in enumerate(line):
                x_pos = self.x + x_offset * 4
                y_pos = self.y + y_offset * 6 
                set_character(canvas, character, (x_pos, y_pos), self.color)

    def update_display(self, canvas, updated_content: list[str]) -> None:
        updated_cells = self.update_display_content(updated_content)

        for x, y in updated_cells:
            character = self.display_content[y][x]
            position = (self.x + x * 4, self.y + y * 6)

            set_character(canvas, character, position, self.color)

    def scroll_display(self, canvas) -> None:
        pass


def set_character(canvas, character: str, position: tuple[int, int], rgb: tuple[int, int, int] = WHITE) -> None:
    if character not in font:
            character = "?"

    char_arr = font[character]
    start_x, start_y = position
    r_on, g_on, b_on = rgb

    for y in range(5):
        for x in range(3):
            r, g, b = (r_on, g_on, b_on) if char_arr[y][x] == 1 else (0, 0, 0)
            
            canvas.SetPixel(start_x + x, start_y + y, r, b, g)