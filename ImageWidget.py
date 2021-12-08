from PIL import ImageQt, Image
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Slot

import SelectionBox


class customScene(QtWidgets.QGraphicsScene):
    def __init(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = SelectionBox.Box(self, 0.0, 0.0)

    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox = SelectionBox.Box(self, event.scenePos().x(), event.scenePos().y())

        print(self.currentBox.getTopLeft().getX(), self.currentBox.getTopLeft().getY())
        print(event.scenePos().x(), event.scenePos().y())

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox.update(event.scenePos().x(), event.scenePos().y())

    def mouseReleaseEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox.update(event.scenePos().x(), event.scenePos().y())

class ImageWidget(QtWidgets.QWidget):  # Central Widget

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

    @Slot()
    def load_image(self, img):
        self.scene = customScene()
        self.view = View(self.scene)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.adjustSize()
        self.setLayout(layout)
        if len(img) > 0:
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
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.scene = parent
