from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsRectItem

from Model.selection_box import Box
from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation


class CustomScene(QtWidgets.QGraphicsScene):
    currentAnnotateImage: AnnotateImage
    rectangle_list: list[QGraphicsRectItem]
    left_click_pressed: bool

    def __init__(self, parentWidget:QtWidgets.QWidget, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = None
        self.parentWidget = parentWidget
        self.parentWidget.setCursor(Qt.CrossCursor)
        self.left_click_pressed = False
        self.rectangle_list = []

    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.currentBox = Box(self, event.scenePos().x(), event.scenePos().y())
            self.left_click_pressed = True

        elif event.button() == Qt.RightButton:

            if len(self.rectangle_list) > 0:
                self.removeItem(self.rectangle_list[-1])
                self.rectangle_list.pop()

            if len(self.currentAnnotateImage.get_annotation_list()) > 0:
                self.currentAnnotateImage.get_annotation_list().pop()

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.left_click_pressed:
            self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.currentBox.update()

    def mouseReleaseEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.currentBox.update()
            self.finishBox()
            self.left_click_pressed = False

    def wheelEvent(self, event:QtWidgets.QGraphicsSceneWheelEvent) -> None:
        # Do nothing, no scrolling allowed here sir (but later we'll maybe use it to zoom in/out
        pass

    def finishBox(self):
        if self.currentBox is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            finalBox = self.currentBox.getBox()
            self.rectangle_list.append(finalBox)
            title = "Default title"
            self.currentAnnotateImage.add_annotation(Annotation(title, finalBox))

    def setCurrentAnnotateImage(self, annotateImage:AnnotateImage):
        self.currentAnnotateImage = annotateImage