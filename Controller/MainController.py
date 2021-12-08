from Model import ModelAnnotator, AnnotateImage
from View import MainWindow
from Controller import ImageWidgetController, ChooseImageAreaController


class MainController:


    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_model = main_model
        self.main_view: MainWindow = main_view

        self.set_menu_bar_action()
        # self.main_view.choose_image_area.itemDoubleClicked.triggered.connect()


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
                # Envoyer les infos à la scroll area
                ChooseImageAreaController.create_button(self.main_view.choose_image_area, image)
                # Envoyer les infos au widget image
                ImageWidgetController.load_image(self.main_view.w, image)

    def delete_image(self, image: AnnotateImage):
        ChooseImageAreaController.delete_button(self.main_view.choose_image_area, image)
        # si dans la graphicView la clear la graphic view
