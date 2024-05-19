class GraphicalElement:
    def __init__(self):
        self.selected: bool = False

    def is_selected(self) -> bool:
        return self.selected

    def set_selected(self, selected: bool):
        self.selected = selected
