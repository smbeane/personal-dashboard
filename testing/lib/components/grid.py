from typing import Tuple, Any, List

from lib.letters import font
from lib.helpers import set_character

WHITE = (255, 255, 255)

NOT_INITIALIZED = [(-1, -1)]

class Grid:
    def __init__(self, position: Tuple[int, int], dims: Tuple[int, int], font_size: str, content: List[str], color: Tuple[int, int, int] = WHITE) -> None:
        self.x, self.y = position
        self.x_len, self.y_len = dims
        self.font_size = font_size #will allow for text to be 3x5, 5x7, or larger?
        self.color = color

        self.full_content = content
        self.offscreen_content = self._init_content(content)
        self.scroll_indexes = [0] * len(self.offscreen_content)

    def initial_render(self, canvas) -> None:
        for y_offset, line in enumerate(self.offscreen_content[:self.y_len]):
            for x_offset, character in enumerate(line[:self.x_len]):
                x_pos = self.x + x_offset * 4
                y_pos = self.y + y_offset * 6
                set_character(canvas, self.font_size, character, (x_pos, y_pos), self.color) 

    def update_and_render(self, canvas: Any, updated_content: List[str]) -> None:
        updated_cells = self._update_content(updated_content, False)

        if not updated_cells:
            if self._needs_scrolled():
                self._scroll_grid_x(canvas)

            return
        
        if updated_cells == NOT_INITIALIZED:
            self.initial_render(canvas)
            return
        
        self.scroll_indexes = [0] * len(self.offscreen_content)
        self._update_render(canvas, updated_cells)
        self.full_content = updated_content

    def _init_content(self, full_content: List[str]) -> List[List[str]]:
        offscreen_content = []
        
        for line in full_content: 
            line = line.ljust(self.x_len)
            line_arr = list(line)

            offscreen_content.append(line_arr)

        return offscreen_content

    def _update_content(self, updated_content: List[str], scrolling: bool) -> List[Tuple[int, int]]:
        if not self.offscreen_content:
            self.offscreen_content = self._init_content(updated_content)
            return NOT_INITIALIZED
        
        if updated_content == self.full_content and not scrolling:
            return []
        
        updated_cells = []

        for y_index in range(len(self.offscreen_content)):
            old_line = self.offscreen_content[y_index]
            new_line = list(updated_content[y_index].ljust(self.x_len))

            if new_line == old_line:
                continue
            
            shorter_len = min(len(old_line), len(new_line))

            for x_index in range(shorter_len):
                old_char = old_line[x_index]
                new_char = new_line[x_index]

                if old_char != new_char:
                    updated_cells.append((x_index, y_index))
                    self.offscreen_content[y_index][x_index] = new_char
            
            if len(old_line) > len(new_line):
                self.offscreen_content[y_index] = self.offscreen_content[y_index][:len(new_line)]
            else: 
                self.offscreen_content[y_index][len(old_line):len(new_line)] = new_line[len(old_line):len(new_line)]
        
        return updated_cells
    
    def _update_render(self, canvas: Any, updated_cells: List[Tuple[int, int]]) -> None:
        for x, y in updated_cells:
            if x >= self.x_len or y >= self.y_len:
                continue
            character = self.offscreen_content[y][x]
            position = (self.x + x * 4, self.y + y * 6)
            set_character(canvas, self.font_size, character, position, self.color)

    def _scroll_grid_x(self, canvas: Any) -> None:
        scrolled_content = []
        all_lines_at_start = all(self.scroll_indexes[index] == 0 for index in range(len(self.scroll_indexes)))

        for index, line in enumerate(self.offscreen_content[:self.y_len]):
            
            if self._line_needs_scrolled(line, index, all_lines_at_start):
                scroll_index = self.scroll_indexes[index]
                scrolled_line = f"{''.join(line[1:])}{line[0]}"
                
                scrolled_content.append(scrolled_line)
                self.scroll_indexes[index] = (scroll_index + 1) % (len(scrolled_line))
            else:
                scrolled_content.append("".join(line))

        updated_cells = self._update_content(scrolled_content, True)
        self._update_render(canvas, updated_cells)

    #TODO
    def _scroll_grid_y(self, canvas: Any) -> None:
        pass

    def _needs_scrolled(self) -> bool:
        return any(len(line) > self.x_len for line in self.full_content[:self.y_len])    

    def _line_needs_scrolled(self, line, line_index, all_lines_at_start) -> bool:
        too_long = len(line) - 2 > self.x_len
        line_at_start = self.scroll_indexes[line_index] == 0

        return too_long and (not line_at_start or all_lines_at_start)
