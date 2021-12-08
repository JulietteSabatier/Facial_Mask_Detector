from View.choose_image_area import ChooseImageArea
from Model.annotate_image import AnnotateImage


def create_button(choose_image_area: ChooseImageArea, image: AnnotateImage):
    choose_image_area.add_image(image.title)


def delete_button(choose_image_area: ChooseImageArea, image: AnnotateImage):
    print("Delete button in scroll area")

