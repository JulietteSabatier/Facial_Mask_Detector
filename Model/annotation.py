from Model.position import Position

# Représente les annotations

class Annotation:
    title: str
    position: Position

    def __init__(self, title, position):
        self.title = title
        self.position = position

    def get_title(self):
        return self.title

    def get_position(self):
        return self.position

    def set_title(self, new_title):
        self.title = new_title

    def set_position(self, new_position):
        self.position = new_position
