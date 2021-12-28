from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator

from View.main_window import MainWindow


class ChooseImageAreaController:
    main_view: MainWindow
    main_model: ModelAnnotator

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        """ Define the functions which permit to update the choose_image_area
        which contains the names of the annotates image"""
        self.main_model = main_model
        self.main_view = main_view

    def create_button(self, image: AnnotateImage):
        """ Function (slot) used to add an item in the list of image """
        self.main_view.choose_image_area.add_image(image.title)

    def delete_button(self):
        """ Function (slot) used to remove an item from the list of image"""
        name_image = self.main_view.choose_image_area.delete_image()
        self.main_model.delete_image_by_name(name_image)

    def rename_button(self):
        """ Function (slot) used to rename an item of the list of image"""
        # Get a new name and change it on the view
        new_name = self.main_view.choose_image_area.rename_image_input()

        # Get the image name
        name_image = self.main_view.choose_image_area.currentItem().text()

        # Change the name of the image in the model
        image = self.main_model.get_image_by_name(name_image)
        image.title = new_name
