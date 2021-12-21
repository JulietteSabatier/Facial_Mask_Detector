from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen

from Model.selection_box import Box
from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation


class CustomScene(QtWidgets.QGraphicsScene):
    currentAnnotateImage: AnnotateImage
    currentBox: Box
    box_list: list[Box]
    left_click_pressed: bool

    def __init__(self, parentWidget:QtWidgets.QWidget, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = None
        self.parentWidget = parentWidget
        self.parentWidget.setCursor(Qt.CrossCursor)
        self.left_click_pressed = False
        self.box_list = []


    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.currentBox = Box(self, event.scenePos().x(), event.scenePos().y())
            self.left_click_pressed = True

        elif event.button() == Qt.RightButton:

            if len(self.box_list) > 0:
                self.removeItem(self.box_list[-1].getBox())
                self.box_list.pop()

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
        # Do nothing, no scrolling allowed here sir (but later we'll maybe use it to zoom in/out)
        pass


    def finishBox(self):
        if self.currentBox is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            title = "Default title"

            # Vérification des box qui seraient plus petites
            boxes_to_remove = []
            for box in self.box_list:
                if min(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) <= min(box.getTopLeft().getX(), box.getBottomRight().getX()) \
                        and min(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()) <= min(box.getTopLeft().getY(), box.getBottomRight().getY()):

                    if max(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) >= max(box.getTopLeft().getX(), box.getBottomRight().getX()) \
                            and max(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()) >= max(box.getTopLeft().getY(), box.getBottomRight().getY()):
                        boxes_to_remove.append(box) # je passe par une liste intermédiaire pour éviter les bugs en modifiant la liste que je parcours

            for box in boxes_to_remove:
                self.removeItem(box.getBox()) # on supprime le rectangle de l'image
                self.box_list.remove(box) # on le retire de la liste actuelle
                self.currentAnnotateImage.remove_annotation(box) # on retire l'annotation qui lui est associée sur l'image

            # Vérification des box qui seraient plus grande
            bigger_box = False
            for box in self.box_list:
                if min(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) >= min(box.getTopLeft().getX(), box.getBottomRight().getX()) \
                        and min(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()) >= min(box.getTopLeft().getY(), box.getBottomRight().getY()):

                    if max(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()) <= max(box.getTopLeft().getX(), box.getBottomRight().getX()) \
                            and max(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()) <= max(box.getTopLeft().getY(), box.getBottomRight().getY()):
                        bigger_box = True

            if bigger_box:
                self.removeItem(self.currentBox.getBox())
            else:
                self.box_list.append(self.currentBox)
                self.currentAnnotateImage.add_annotation(Annotation(title, self.currentBox))


    def setCurrentAnnotateImage(self, annotateImage:AnnotateImage):
        self.currentAnnotateImage = annotateImage

    def loadAnnotations(self):
        self.box_list = []

        for annotation in self.currentAnnotateImage.get_annotation_list():
            self.box_list.append(annotation.get_box())

        for box in self.box_list:
            box.setBox(self.addRect(box.getTopLeft().getX(), box.getTopLeft().getY(), box.getWidth(), box.getHeight(), QPen(Qt.blue)))