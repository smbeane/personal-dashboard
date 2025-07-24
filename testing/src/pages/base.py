class BaseScreen:
    def __init__(self, canvas):
        self.canvas = canvas
        self.page_active = False
    
    def update_data(self):
        pass

    def render_screen(self):
        pass

    