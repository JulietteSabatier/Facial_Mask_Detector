import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, Image
from PySide6.QtCore import Slot, Qt


class ImageWidget(QtWidgets.QWidget):  # Central Widget

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = View(self.scene)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.adjustSize()
        self.setLayout(layout)

    @Slot()
    def load_image(self, img):
        self.scene.clear()
        imgPath = img[0]
        image = Image.open(imgPath)
        w, h = image.size
        self.imgQ = ImageQt.ImageQt(image)  # we need to hold reference to imgQ
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.scene.update()


class View(QtWidgets.QGraphicsView):  # view of the image
    def mousePressEvent(self, event):
        print("QGraphicsView mousePress")

    def mouseMoveEvent(self, event):
        print("QGraphicsView mouseMove")

    def mouseReleaseEvent(self, event):
        print("QGraphicsView mouseRelease")
