import os.path
import csv, json

from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation
from Model.selection_box import Box
from Model.category import Category

# Représente les data (liste de catégories et d'images annotés)

class ModelAnnotator:
    category_list: list[Category]
    image_list: list[AnnotateImage]

    def __init__(self, category_list: (list[Category]), image_list: (list[AnnotateImage])):
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
            image.save_image(new_path)
            image.path = new_path + image.title + ".png"

    # Category
    def get_category_list(self):
        return self.category_list

    def get_category_by_name(self, name: str):
        for category in self.category_list:
            if category.name == name:
                return category

    def add_category(self, name: str):
        for cat in self.category_list:
            if cat.name == name:
                return
        category = Category(name)
        self.category_list.append(category)

    def delete_category(self, category: str):
        for cat in self.category_list:
            if cat.name == category:
                self.category_list.remove(cat)

    def rename_category(self, category: str, new_name: str):
        for cat in self.category_list:
            if cat.name == category:
                cat.name = new_name
                return

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
            data["categories"].append(cat.name)
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
                data[image.title]["annotations"].append(annotation.from_annotations_to_json())
        json_file = open(path, 'w')
        json.dump(data, json_file)

    def from_json_to_annotation(self, path: str):
        f = open(path)
        json_data = json.load(f)
        if len(json_data) != 0:
            for image in json_data:
                if os.path.exists(json_data[image]["path"]):
                    annotations = []
                    annotate_image = AnnotateImage(json_data[image]["path"], image, annotations)
                    if len(json_data[image]["annotations"]) != 0:
                        for i in range(len(json_data[image]["annotations"])):

                            top_x = json_data[image]["annotations"][i]["box"]["top_left"]["abs"]
                            top_y = json_data[image]["annotations"][i]["box"]["top_left"]["ord"]
                            box = Box(None, top_x, top_y)
                            bottom_x = json_data[image]["annotations"][i]["box"]["bottom_right"]["abs"]
                            bottom_y = json_data[image]["annotations"][i]["box"]["bottom_right"]["ord"]
                            box.updateBottomRight(bottom_x, bottom_y)
                            category = Category(json_data[image]["annotations"][i]["title"])
                            annotations.append(Annotation(category, box))
                        self.add_image(annotate_image)
        f.close()
