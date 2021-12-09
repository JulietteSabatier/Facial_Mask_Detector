from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator

from Controller.choose_image_area_controller import ChooseImageAreaController
from Controller.image_widget_controller import ImageWidgetController
from View.main_window import MainWindow


# Définition des fonctions qui représentent les action de la menuBar


class MenuBarController:
    main_view: MainWindow
    main_model: ModelAnnotator

    choose_image_area_controller: ChooseImageAreaController
    image_widget: ImageWidgetController

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        self.main_view = main_view
        self.main_model = main_model


    def show_all_categories(self):
        return 0


    def load_image_menu_bar(self):

        # Charge un ou plusieurs images la dernière seulement s'affiche dans la graphicView
        # Ne charge pas les annotations
        imgs = self.main_view.menu_bar.widget_load_image()

        if len(imgs[0]) != 0:

            for i in range(len(imgs[0])):
                path = imgs[0][i]
                title = path.split("/")[-1].split(".")[0]
                image = AnnotateImage(path, title, [])

                # Ajouter l'image dans la base
                self.main_model.add_image(image)
                # Envoyer les infos a la scroll area
                ChooseImageAreaController.create_button(self.main_view.choose_image_area, image)
                # Envoyer les infos a au widget image
                ImageWidgetController.load_image(self, image)
