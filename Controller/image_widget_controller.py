from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from PIL import Image, ImageQt
from PySide6 import QtCore, QtGui
from View.main_window import MainWindow

# Définition des fonctions qui permettent de mettre a jour le widget contenant les images

class ImageWidgetController:
    main_view: MainWindow
    main_model: ModelAnnotator

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        self.main_view = main_view
        self.main_model = main_model

    def load_image_widget(self, image: AnnotateImage):
        self.main_view.image_widget.initialize_scene()

        self.main_view.image_widget.scene.setCurrentAnnotateImage(image)

        img_path = image.path
        image = Image.open(img_path)
        w, h = image.size
        img_q = ImageQt.ImageQt(image)
        pixmap = QtGui.QPixmap.fromImage(img_q)
        self.main_view.image_widget.scene.addPixmap(pixmap)
        self.main_view.image_widget.view.fitInView(QtCore.QRect(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.main_view.image_widget.scene.update()
        self.main_view.image_widget.scene.loadAnnotations()
