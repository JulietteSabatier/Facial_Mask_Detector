from PySide6.QtCore import Slot
from PIL import Image, ImageQt
from PySide6 import QtGui
from PySide6 import QtCore

from Model import AnnotateImage
from Model import ModelAnnotator
from View import MainWindow


class MenuBarController:

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_model = main_model
        self.main_view = main_view

    @Slot()
    def print_load_image(self):
        print("load image")

    @Slot()
    def load_image_function(self):
        img = self.main_view.menu_bar.widget_load_image()

        if len(img) != 0:
            path = img[0][0]
            title = path.split("/")[-1].split(".")[0]
            image = AnnotateImage.AnnotateImage(path, title, [])

            # Ajouter l'image dans la base
            self.main_model.add_image(image)

            # Envoyer les infos a la scroll area
            self.main_view.get_choose_image_area().add_image(image.title)

            # Envoyer les infos a au widget image
            self.main_view.w.scene.clear()
            img_path = image.path
            image = Image.open(img_path)
            w, h = image.size
            img_q = ImageQt.ImageQt(image)
            pixmap = QtGui.QPixmap.fromImage(img_q)
            self.main_view.w.scene.addPixmap(pixmap)
            self.main_view.w.view.fitInView(QtCore.QRect(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            self.main_view.w.scene.update()
