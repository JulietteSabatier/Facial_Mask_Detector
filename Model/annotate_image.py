from Model.annotation import Annotation
from PIL import Image

# Représentation des images annotées

class AnnotateImage:
    path: str
    title: str
    annotation_list: list[Annotation]

    def __init__(self, path: str, title: str, annotation_list: list[Annotation]):
        self.title = title
        self.path = path
        self.annotation_list = annotation_list

    def add_annotation(self, annotation: Annotation) -> None:
        self.annotation_list.append(annotation)

    def remove_annotation(self, box):
        for annotation in self.annotation_list:
            if annotation.get_box().getTopLeft() == box.getTopLeft() and annotation.get_box().getBottomRight() == box.getBottomRight():
                self.annotation_list.remove(annotation)

    def get_path(self):
        return self.path

    def get_title(self):
        return self.title

    def get_annotation_list(self):
        return self.annotation_list

    def set_title(self, title: str):
        self.title = title

    def set_path(self, path: str):
        self.path = path

    def set_annotation_list(self, annotation_list: list[Annotation]):
        self.annotation_list = annotation_list

    def save_image(self, path: str):
        image = Image.open(self.path, 'r')
        image.save(path + "/" + self.title + ".png")
