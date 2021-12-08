from PIL import ImageQt, Image
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Slot

import Box


class ImageWidget(QtWidgets.QWidget):  # Central Widget

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = View(self.scene)
        self.view.setSceneRect(QtCore.QRectF(0, 0, self.scene.width(), self.scene.height()))
        # cette ligne positionne les rectangle correctement (sur une scene vide uniquement) mais casse le layout global
        # self.view.setSceneRect(QtCore.QRectF(0, 0, self.width(), self.height()))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.adjustSize()
        self.setLayout(layout)

    @Slot()
    def load_image(self, img):
        if len(img) > 0:
            self.scene.clear()
            imgPath = img[0]
            image = Image.open(imgPath)
            w, h = image.size
            self.imgQ = ImageQt.ImageQt(image)  # we need to hold reference to imgQ
            pixMap = QtGui.QPixmap.fromImage(self.imgQ)
            self.scene.addPixmap(pixMap)
            self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            self.view.setSceneRect(QtCore.QRectF(0, 0, w, h))
        self.scene.update()


class View(QtWidgets.QGraphicsView):  # view of the image
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.scene = parent
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.currentBox = Box.Box(self.scene, 0.0, 0.0)

    def mousePressEvent(self, event):
        self.currentBox = Box.Box(self.scene, event.pos().x(), event.pos().y())

        print(self.currentBox.getTopLeft().getX(), self.currentBox.getTopLeft().getY())
        print(event.pos().x(), event.pos().y())


    def mouseMoveEvent(self, event):
        self.currentBox.update(event.pos().x(), event.pos().y())


    def mouseReleaseEvent(self, event):
        self.currentBox.update(event.pos().x(), event.pos().y())
