import Model.AnnotateImage as Image


class ModelAnnotator:
    category_list: list[str]
    image_list: list[Image]

    def __init__(self, category_list: (list[str]), image_list: (list[Image])):
        self.category_list = category_list
        self.image_list = image_list

    def get_category_list(self):
        return self.category_list

    def get_image_list(self):
        return self.image_list

    def add_image(self, image: Image):
        self.image_list.append(image)

    def delete_image(self, image: Image):
        self.image_list.remove(image)

    def delete_image_by_name(self, name: str):
        for image in self.image_list:
            if image.get_title() == name:
                self.image_list.remove(image)
                break

    def delete_category(self, category: str):
        self.category_list.remove(category)



