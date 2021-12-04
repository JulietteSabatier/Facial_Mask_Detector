from Model import ModelAnnotator, AnnotateImage
from View import MainWindow
from Controller import ImageWidgetController, ChooseImageAreaController


class MainController:
    main_model: ModelAnnotator
    main_view: MainWindow

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_model = main_model
        self.main_view = main_view

        self.set_menu_bar_action()

    def set_menu_bar_action(self):
        self.main_view.menu_bar.image.load_image.triggered.connect(self.load_new_images)

    def load_new_images(self):
        # Charge un ou plusieurs images la dernière seulement s'affiche dans la graphicView
        # Ne charge pas les annotations
        imgs = self.main_view.menu_bar.widget_load_image()

        if len(imgs[0]) != 0:

            for i in range(len(imgs[0])):
                path = imgs[0][i]
                title = path.split("/")[-1].split(".")[0]
                image = AnnotateImage.AnnotateImage(path, title, [])

                # Ajouter l'image dans la base
                self.main_model.add_image(image)
                # Envoyer les infos a la scroll area
                ChooseImageAreaController.create_button(self.main_view.c, image)
                # Envoyer les infos a au widget image
                ImageWidgetController.load_image(self.main_view.w, image)

