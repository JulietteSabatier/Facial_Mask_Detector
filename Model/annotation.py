from Model.selection_box import Box
from Model.category import Category


class Annotation:
    title: Category
    box: Box

    def __init__(self, title: Category, box: Box):
        """ Create an Annotation composed by a title (Category) and a box (Box)
         which represent the position of the annotation in the box """
        self.title = title
        self.box = box

    def get_title(self):
        """ Return the name of the category of the annotation """
        return self.title

    def get_box(self):
        """ Return the box of the annotation """
        return self.box

    def set_title(self, new_title: Category):
        """ Set the title/category of the annotation """
        self.title = new_title

    def from_annotations_to_json(self):
        """ Return the annotation convert in a json format """
        if self.title is None:
            return {"title": "", "box": self.box.get_position_as_json()}
        else:
            return {"title": self.title.name,
                    "box": self.box.get_position_as_json()}
