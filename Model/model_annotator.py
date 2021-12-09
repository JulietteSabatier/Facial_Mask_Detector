from Model.annotate_image import AnnotateImage

# Représente les data (liste de catégories et d'images annotés)

class ModelAnnotator:
    category_list: list[str]
    image_list: list[AnnotateImage]

    def __init__(self, category_list: (list[str]), image_list: (list[AnnotateImage])):
        self.category_list = category_list
        self.image_list = image_list

    def get_category_list(self):
        return self.category_list

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

    def delete_category(self, category: str):
        self.category_list.remove(category)

    def get_image_by_name(self, name: str):
        for i in range(len(self.image_list)):
            if self.image_list[i].title == name:
                return self.image_list[i]
        return None

