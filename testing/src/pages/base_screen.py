class BaseScreen:
    def __init__(self, canvas):
        self.canvas = canvas
        self.page_active = False
    
    def update(self) -> None:
        pass
    
    def update_data(self) -> None:
        pass

    def init_page(self) -> None:
        pass

    def update_page(self) -> None:
        pass

    