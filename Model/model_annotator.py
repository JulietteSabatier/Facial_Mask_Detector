import os.path

from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation
from Model.position import Position
import csv, json
from PIL import Image


# Représente les data (liste de catégories et d'images annotés)

class ModelAnnotator:
    category_list: list[str]
    image_list: list[AnnotateImage]

    def __init__(self, category_list: (list[str]), image_list: (list[AnnotateImage])):
        self.category_list = category_list
        self.image_list = image_list

    # Image
    def get_image_list(self):
        return self.image_list

    def add_image(self, image: AnnotateImage):
        self.image_list.append(image)

    def delete_image(self, image: AnnotateImage):
        self.image_list.remove(image)

    def delete_image_by_name(self, name: str):
        for image in self.image_list:
            if image.get_title() == name:
                self.image_list.remove(image)
                break

    def get_image_by_name(self, name: str):
        for i in range(len(self.image_list)):
            if self.image_list[i].title == name:
                return self.image_list[i]
        return None

    def save_images(self, new_path: str):
        for image in self.image_list:
            path = image.path
            image.save_image(path, new_path)

    # Category
    def get_category_list(self):
        return self.category_list

    def add_category(self, name: str):
        if not self.category_list.__contains__(name):
            self.category_list.append(name)

    def delete_category(self, category: str):
        self.category_list.remove(category)

    def rename_category(self, category: str, new_name: str):
        for i in range(len(self.category_list)):
            if self.category_list[i] == category:
                self.category_list[i] = new_name
        # Change in the annotations too
        # Maybe create an object annotation to change easily the name without
        # search the name in all the annotations

    def from_csv_to_categories(self, path: str):
        csv_file = open(path)
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            for col in range(len(row)):
                self.add_category(row[col])

    def from_json_to_categories(self, path: str):
        json_file = open(path)
        data = json.load(json_file)
        if len(data) != 0:
            for cat in data['categories']:
                self.add_category(cat)

    def from_categories_to_json(self, path: str):
        data = {"categories": []}
        for cat in self.category_list:
            data["categories"].append(cat)
        try:
            json_file = open(path, 'w')
            json.dump(data, json_file)
        except:
            return

    # Annotations
    def from_annotation_to_json(self, path: str):
        data = {}
        for image in self.image_list:
            data[image.title] = {"path": image.path,
                                 "annotations": []}
            for annotation in image.annotation_list:
                data[image.title]["annotations"] = annotation.from_annotations_to_json()
        json_file = open(path, 'w')
        json.dump(data, json_file)

    def from_json_to_annotation(self, path: str):
        f = open(path)
        json_data = json.load(f)
        if len(json_data) != 0:
            for image in json_data:
                print(image)
                if os.path.exists(json_data[image]["path"]):
                    annotations = []
                    for annotation in json_data[image]["annotations"]:
                        position = Position(
                            (annotation["position"]["left_up"]["abs"], annotation["position"]["left_up"]["ord"]),
                            (annotation["position"]["right_down"]["abs"], annotation["position"]["right_down"]["ord"]))
                        annotations.append(Annotation(annotation["title"], position))
                    annotate_image = AnnotateImage(json_data[image]["path"], image, annotations)
                    self.add_image(annotate_image)
        f.close()
