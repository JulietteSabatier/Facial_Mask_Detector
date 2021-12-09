from View.choose_image_area import ChooseImageArea
from Model.annotate_image import AnnotateImage
from View.main_window import MainWindow
from Model.model_annotator import ModelAnnotator


# Définition des fonction qui permettent de mettre a jour la scroll bar des nom d'image

class ChooseImageAreaController:
    main_view: MainWindow
    main_model: ModelAnnotator

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        self.main_model = main_model
        self.main_view = main_view



    def create_button(choose_image_area: ChooseImageArea, image: AnnotateImage):
        choose_image_area.add_image(image.title)

    def delete_button(self):
        print("Delete button in scroll area")
