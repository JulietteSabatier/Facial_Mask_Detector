from Model.annotation import Annotation
from PIL import Image

# Représentation des images annotées

class AnnotateImage:
    path: str
    title: str
    annotation_list: list[Annotation]

    def __init__(self, path: str, title: str, annotation_list: list[Annotation]):
        """ Create an annotate image composed by a name (str), a path (str)
         and a list of Annotation (list[Annotation])"""
        self.title = title
        self.path = path
        self.annotation_list = annotation_list

    def add_annotation(self, annotation: Annotation) -> None:
        """ Add the given annotation in the list of annotation of the annotate image"""
        self.annotation_list.append(annotation)

    def remove_annotation(self, box):
        """" Remove the annotation coresponding to the given box from the list of annotation of the annotate image"""
        for annotation in self.annotation_list:
            if annotation.get_box().getTopLeft() == box.getTopLeft() and annotation.get_box().getBottomRight() == box.getBottomRight():
                self.annotation_list.remove(annotation)

    def get_path(self):
        """ Return the path of the image"""
        return self.path

    def get_title(self):
        """ Return the name/title of the image in the program"""
        return self.title

    def get_annotation_list(self):
        """ Return the list of annotation of the image"""
        return self.annotation_list

    def set_title(self, title: str):
        """ Set the title of the image given the string given in parameter"""
        self.title = title

    def set_path(self, path: str):
        """ Set the path of the image given the string given in parameter"""
        self.path = path

    def set_annotation_list(self, annotation_list: list[Annotation]):
        """ Set the annotation list of the image with the one given in parameter"""
        self.annotation_list = annotation_list

    def save_image(self, new_path: str):
        """ Copy the image on the directory given in parameter"""
        image = Image.open(r''+self.path)
        image.save(new_path+"/"+self.title+".png")
        image.close()
