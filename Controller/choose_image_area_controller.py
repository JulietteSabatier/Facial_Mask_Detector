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

    def create_button(self, image: AnnotateImage):

        self.main_view.choose_image_area.add_image(image.title)

    def delete_button(self):
        name_image = self.main_view.choose_image_area.delete_image()
        self.main_model.delete_image_by_name(name_image)

    def rename_button(self):
        # Get a new name and change it on the view
        new_name = self.main_view.choose_image_area.rename_image_input()

        # Get the image name
        name_image = self.main_view.choose_image_area.currentItem().text()

        # Change the name of the image in the model
        image = self.main_model.get_image_by_name(name_image)
        image.title = new_name
