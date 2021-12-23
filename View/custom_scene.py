from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6 import QtCore
from Model.selection_box import Box
from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation


class CustomScene(QtWidgets.QGraphicsScene):
    currentAnnotateImage: AnnotateImage
    currentBox: Box
    currentRect: QtWidgets.QGraphicsRectItem
    box_list: list[Box]
    left_click_pressed: bool

    def __init__(self, parentWidget: QtWidgets.QWidget, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = None
        self.currentRect = None
        self.parentWidget = parentWidget
        self.parentWidget.setCursor(Qt.CrossCursor)
        self.left_click_pressed = False
        self.box_list = []

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.currentBox = Box(self, event.scenePos().x(), event.scenePos().y())
            self.currentRect = self.addRect(event.scenePos().x(), event.scenePos().y(), 0, 0, QPen(Qt.blue))
            self.left_click_pressed = True

        elif event.button() == Qt.RightButton:

            if len(self.box_list) > 0:
                self.removeItem(self.box_list[-1].getBox())
                self.box_list.pop()

            if len(self.currentAnnotateImage.get_annotation_list()) > 0:
                self.currentAnnotateImage.get_annotation_list().pop()

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.left_click_pressed:
            self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.currentRect.setRect(
                self.currentBox.getTopLeft().x,
                self.currentBox.getTopLeft().y,
                abs(self.currentBox.getTopLeft().getX() - event.scenePos().x()),
                abs(self.currentBox.getTopLeft().getY() - event.scenePos().y()))
            self.currentBox.update()

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.currentRect.setRect(
                self.currentBox.getTopLeft().x,
                self.currentBox.getTopLeft().y,
                abs(self.currentBox.getTopLeft().getX() - event.scenePos().x()),
                abs(self.currentBox.getTopLeft().getY() - event.scenePos().y()))
            self.currentBox.update()
            self.finishBox()
            self.left_click_pressed = False

    def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent) -> None:
        # Do nothing, no scrolling allowed here sir (but later we'll maybe use it to zoom in/out)
        pass

    def finishBox(self):
        if self.currentBox is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            title = "Default title"

            is_invalid = False
            for box in self.box_list:
                # Vérification des box qui seraient plus petites
                if min(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) <= min(
                        box.getTopLeft().getX(), box.getBottomRight().getX()) \
                        and min(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()) <= min(
                    box.getTopLeft().getY(), box.getBottomRight().getY()):

                    if max(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) >= max(
                            box.getTopLeft().getX(), box.getBottomRight().getX()) \
                            and max(self.currentBox.getTopLeft().getY(),
                                    self.currentBox.getBottomRight().getY()) >= max(box.getTopLeft().getY(),
                                                                                    box.getBottomRight().getY()):
                        is_invalid = True

                # Vérification des box qui seraient plus grande (le code est pas dupliqué, je sais pas pourquoi PyCharm dit le contraire)
                if min(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) >= min(
                        box.getTopLeft().getX(), box.getBottomRight().getX()) \
                        and min(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()) >= min(
                    box.getTopLeft().getY(), box.getBottomRight().getY()):

                    if max(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) <= max(
                            box.getTopLeft().getX(), box.getBottomRight().getX()) \
                            and max(self.currentBox.getTopLeft().getY(),
                                    self.currentBox.getBottomRight().getY()) <= max(box.getTopLeft().getY(),
                                                                                    box.getBottomRight().getY()):
                        is_invalid = True

            if is_invalid:
                self.removeItem(self.currentBox.getBox())
            else:
                annotation = Annotation(title, self.currentBox)
                self.box_list.append(self.currentBox)
                self.currentAnnotateImage.add_annotation(annotation)
                # self.addAnnotation(annotation)

    def setCurrentAnnotateImage(self, annotateImage: AnnotateImage):
        self.currentAnnotateImage = annotateImage

    def loadAnnotations(self):
        for annotation in self.currentAnnotateImage.get_annotation_list():
            self.addAnnotation(annotation)

    def addAnnotation(self, annotation: Annotation):
        box = annotation.get_box()
        top_left = box.getTopLeft()
        bottom_right = box.getBottomRight()

        self.box_list.append(box)
        self.addRect(top_left.getX(), top_left.getY(),
                     abs(bottom_right.getX() - top_left.getX()), abs(top_left.getY() - bottom_right.getY()),
                     QPen(Qt.blue))
