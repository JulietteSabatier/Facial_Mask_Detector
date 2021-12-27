import Model.position as Position
from Model.selection_box import Box
from Model.category import Category


class Annotation:
    title: Category
    box: Box

    def __init__(self, title: Category, box: Box):
        self.title = title
        self.box = box

    def get_title(self):
        return self.title

    def get_box(self):
        return self.box

    def set_title(self, new_title: Category):
        self.title = new_title

    def from_annotations_to_json(self):
        return {"title": self.title.name,
                "box": self.box.get_position_as_json()}
