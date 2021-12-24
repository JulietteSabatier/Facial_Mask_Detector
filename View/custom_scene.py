import shapely.geometry
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6 import QtCore
from Model.selection_box import Box
from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation
from View.view import View


class CustomScene(QtWidgets.QGraphicsScene):
    currentAnnotateImage: AnnotateImage
    currentBox: Box
    currentRect: QtWidgets.QGraphicsRectItem
    box_list: list[Box]
    left_click_pressed: bool
    view: View

    def __init__(self, parentWidget: QtWidgets.QWidget, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = None
        self.currentRect = None
        self.parentWidget = parentWidget
        self.parentWidget.setCursor(Qt.CrossCursor)
        self.left_click_pressed = False
        self.box_list = []


    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        #Left click = creating a new box
        if event.button() == Qt.LeftButton:
            if self.currentBox is not None:
                self.currentBox.getBox().setSelected(False)

            self.currentBox = Box(self, event.scenePos().x(), event.scenePos().y())
            self.currentRect = self.addRect(event.scenePos().x(), event.scenePos().y(), 0, 0, QPen(Qt.blue))

            self.left_click_pressed = True

        #Right click = removing the most recently registered box
        elif event.button() == Qt.RightButton:
            comboBox = QtWidgets.QInputDialog.setComboBoxEditable(True)

        #    if len(self.box_list) > 0:
        #        self.removeItem(self.box_list[-1].getBox())
        #        self.box_list.pop()

        #    if len(self.currentAnnotateImage.get_annotation_list()) > 0:
        #        self.currentAnnotateImage.get_annotation_list().pop()

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        # If the left click is pressed (we must not do it with right click), we update the box we're creating
        if self.left_click_pressed:
            self.updateRect(event.scenePos().x(), event.scenePos().y())

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        # If it's the left click (we don't care about the right click), we update the box one last time
        # and then call the function to check its final validity
        if event.button() == Qt.LeftButton and self.currentBox is not None and not self.currentBox.getBox().isSelected():
            self.updateRect(event.scenePos().x(), event.scenePos().y())
            self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.currentBox.update()
            self.finishBox()
            self.left_click_pressed = False

    def mouseDoubleClickEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            for box in self.box_list:
                if box.getBox().contains(event.scenePos()):
                    box.getBox().setSelected(True)
                    self.currentBox = box
                    break


    def wheelEvent(self, event:QtWidgets.QGraphicsSceneWheelEvent) -> None:
        # Do nothing, no scrolling allowed here sir (but later we'll maybe use it to zoom in/out)
        pass

    def updateRect(self, x, y):
        self.currentBox.updateBottomRight(x, y)
        self.currentRect.setRect(
            self.currentBox.getTopLeft().x,
            self.currentBox.getTopLeft().y,
            x - self.currentBox.getTopLeft().getX(),
            y - self.currentBox.getTopLeft().getY())
        self.currentBox.update()

    def popup_rename(self):
        dialog = QtWidgets.QInputDialog().
        dialog.setComboBoxEditable()
        dialog.show()

    def finishBox(self):
        """Does the final verifications to check the validity of the currentBox,
        and either discards it or adds it to the list of boxes and the image annotations.
        A box is discarded if it covers or is covered by another box, if it intersects for more than 20%
        of its surface or the surface of the box it intersects with, if the box area is less than 40 pixels, or if
        one of its border is less than 5 pixels long."""

        if self.currentBox is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            title = "Default title"

            # Vérification de la taille minimale en pixel
            is_invalid = self.view.check_pixel_size(self.currentBox)

            if is_invalid:
                self.removeItem(self.currentBox.getBox())
                print("Box invalide (surface inférieure à 40 pixels ou largeur/longueur inférieure à 5 pixels")
            else:
                new_polygon = shapely.geometry.box(min(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()),
                                                   min(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()),
                                                   max(self.currentBox.getTopLeft().getX(), self.currentBox.getBottomRight().getX()),
                                                   max(self.currentBox.getTopLeft().getY(), self.currentBox.getBottomRight().getY()))
                for box in self.box_list:
                    current_polygon = shapely.geometry.box(min(box.getTopLeft().getX(), box.getBottomRight().getX()),
                                                           min(box.getTopLeft().getY(), box.getBottomRight().getY()),
                                                           max(box.getTopLeft().getX(), box.getBottomRight().getX()),
                                                           max(box.getTopLeft().getY(), box.getBottomRight().getY()))
                    # Vérification des box qui seraient plus petites
                    if new_polygon.covers(current_polygon):
                        is_invalid = True
                        print("Box invalide (couvre une autre box)")
                        break

                    # Vérification des box qui seraient plus grande (le code est pas dupliqué, je sais pas pourquoi PyCharm dit le contraire)
                    if current_polygon.covers(new_polygon):
                        is_invalid = True
                        print("Box invalide (est couverte par une autre)")
                        break

                    # Vérification des box qui seraient couvertes à 40%
                    if new_polygon.intersection(current_polygon).area >= current_polygon.area * 0.2 or new_polygon.intersection(current_polygon).area >= new_polygon.area * 0.2:
                        is_invalid = True
                        print("Box invalide (intersection couvrant 20% ou plus de la surface)")
                        break

            #Oui je vérifie 2 fois mais soit je suis trop bête pour le faire efficacement, soit on peut pas parce qu'on
            #change le booléen après la première vérification
            if is_invalid:
                self.removeItem(self.currentRect)
            else:
                annotation = Annotation(title, self.currentBox)
                self.box_list.append(self.currentBox)
                self.currentAnnotateImage.add_annotation(Annotation(title, self.currentBox))
                self.currentBox.getBox().setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)


    def setCurrentAnnotateImage(self, annotateImage: AnnotateImage):
        self.currentAnnotateImage = annotateImage

    def loadAnnotations(self):
        """Loads the annotations from the current annotate image. For the scene, it means loading the list of boxes to display as rectangles"""
        self.box_list = []

        for annotation in self.currentAnnotateImage.get_annotation_list():
            box = annotation.get_box()
            top_left = box.getTopLeft()
            bottom_right = box.getBottomRight()

        for box in self.box_list:
            box.setBox(self.addRect(box.getTopLeft().getX(), box.getTopLeft().getY(), box.getWidth(), box.getHeight(), QPen(Qt.blue)))
            box.getBox().setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    def set_view(self, view: View):
        self.view = view
            self.box_list.append(box)
            self.addRect(top_left.getX(), top_left.getY(),
                         abs(bottom_right.getX() - top_left.getX()), abs(top_left.getY() - bottom_right.getY()),
                         QPen(Qt.blue))

    def getCurrentAnnotateImage(self):
        return self.currentAnnotateImage

    def getCurrentBox(self):
        return self.currentBox



class PopupComboBox(QtWidgets.QDialog):
     def __init__(self):
         super(PopupComboBox, self).__init__()
         self.resize(400,200)

         self.combo_box = QtWidgets.QComboBox()

         self.box = QtWidgets.QVBoxLayout()
         self.box.addWidget(self.combo_box)
         self.setLayout(self.box)


