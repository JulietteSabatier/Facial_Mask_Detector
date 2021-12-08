from View import ImageWidget
from Model import AnnotateImage
from PIL import Image, ImageQt
from PySide6 import QtGui, QtCore, QtWidgets


def load_image(image_widget: ImageWidget, image: AnnotateImage):
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(image_widget.view)
    image_widget.adjustSize()
    image_widget.setLayout(layout)

    image_widget.scene.clear()
    img_path = image.path
    image = Image.open(img_path)
    w, h = image.size
    img_q = ImageQt.ImageQt(image)
    pixmap = QtGui.QPixmap.fromImage(img_q)
    image_widget.scene.addPixmap(pixmap)
    image_widget.view.fitInView(QtCore.QRect(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
    image_widget.scene.update()

    # If annotations load annotation
