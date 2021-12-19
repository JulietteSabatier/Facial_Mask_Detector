from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from Model.selection_box import Box
from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation


class CustomScene(QtWidgets.QGraphicsScene):
    currentAnnotateImage: AnnotateImage

    def __init__(self, parentWidget:QtWidgets.QWidget, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = None
        self.parentWidget = parentWidget
        self.parentWidget.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox = Box(self, event.scenePos().x(), event.scenePos().y())

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
        self.currentBox.update()

    def mouseReleaseEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
        self.currentBox.update()
        self.finishBox()

    def wheelEvent(self, event:QtWidgets.QGraphicsSceneWheelEvent) -> None:
        # Do nothing, no scrolling allowed here sir (but later we'll maybe use it to zoom in/out
        pass

    def finishBox(self):
        if self.currentBox is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            finalBox = self.currentBox.getBox()
            title = "Default title"
            self.currentAnnotateImage.add_annotation(Annotation(title, finalBox))
            self.currentBox = None

    def setCurrentAnnotateImage(self, annotateImage:AnnotateImage):
        self.currentAnnotateImage = annotateImage