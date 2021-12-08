from PIL import ImageQt, Image
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Slot

from View import SelectionBox


class ImageWidget(QtWidgets.QWidget):  # Central Widget

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = customScene()
        self.view = View(self.scene)


class customScene(QtWidgets.QGraphicsScene):
    def __init(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = SelectionBox.Box(self, 0.0, 0.0)

    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox = SelectionBox.Box(self, event.scenePos().x(), event.scenePos().y())

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox.update(event.scenePos().x(), event.scenePos().y())

    def mouseReleaseEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox.update(event.scenePos().x(), event.scenePos().y())


class View(QtWidgets.QGraphicsView):  # view of the image
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.scene = parent
