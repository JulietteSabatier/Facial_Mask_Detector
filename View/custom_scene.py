from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6 import QtCore, QtGui, QtWidgets

import shapely.geometry

from Model.selection_box import Box
from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation
from Model.model_annotator import ModelAnnotator

from View.view import View
from View.popup_box import PopupBox

from Controller.popup_box_controller import PopupBoxController


class CustomScene(QtWidgets.QGraphicsScene):
    currentAnnotateImage: AnnotateImage
    currentBox: Box
    currentRect: QtWidgets.QGraphicsRectItem
    currentAnnot: Annotation
    box_list: list[Box]
    rect_list: list[QtWidgets.QGraphicsRectItem]
    annot_list: list[Annotation]
    left_click_pressed: bool
    view: View
    main_model: ModelAnnotator

    mouse_press = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)
    mouse_move = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)
    mouse_release = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)
    mouse_double_click = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)

    def __init__(self, model: ModelAnnotator, parentWidget: QtWidgets.QWidget, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.currentBox = None
        self.currentRect = None
        self.parentWidget = parentWidget
        self.parentWidget.setCursor(Qt.CrossCursor)
        self.left_click_pressed = False
        self.box_list = []
        self.rect_list = []
        self.annot_list = []
        self.main_model = model

        self.mouse_press = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)
        self.mouse_move = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)
        self.mouse_release = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)
        self.mouse_double_click = QtCore.Signal(QtWidgets.QGraphicsSceneEvent)

    def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent) -> None:
        # Do nothing, no scrolling allowed here sir (but later we'll maybe use it to zoom in/out)
        pass

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        # Left click = creating a new box
        if event.button() == QtCore.Qt.LeftButton:
            if self.currentRect is not None:
                self.currentRect.setSelected(False)

            self.currentBox = Box(self, event.scenePos().x(), event.scenePos().y())
            self.currentRect = self.addRect(event.scenePos().x(),
                                            event.scenePos().y(),
                                            0, 0,
                                            QtGui.QPen(QtCore.Qt.blue))
            self.left_click_pressed = True

        # Right click = removing the most recently registered box
        # elif event.button() == Qt.RightButton:
        #    comboBox = QtWidgets.QInputDialog.setComboBoxEditable(True)

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
        if event.button() == QtCore.Qt.LeftButton \
                and self.currentRect is not None \
                and not self.currentRect.isSelected():
            self.updateRect(event.scenePos().x(), event.scenePos().y())
            self.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.currentBox.update()
            self.finishBox()
            self.left_click_pressed = False

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            for rect in self.rect_list:
                if rect.contains(event.scenePos()):
                    rect.setSelected(True)
                    self.currentRect = rect
                    index = self.rect_list.index(self.currentRect)
                    self.currentBox = self.box_list.__getitem__(index)
                    self.currentAnnot = self.annot_list.__getitem__(index)
                    self.popup = PopupBox(self.currentAnnot,
                                          self.currentBox, self.box_list,
                                          self.currentRect, self.rect_list,
                                          self.currentAnnot, self.annot_list,
                                          self.main_model,
                                          self.currentAnnotateImage,
                                          self)
                    print("double click on annot0, ", self.currentAnnot.title)
                    break

    def updateRect(self, x, y):
        self.currentBox.update()
        self.currentRect.setRect(
            self.currentBox.getTopLeft().getX(),
            self.currentBox.getTopLeft().getY(),
            x - self.currentBox.getTopLeft().getX(),
            y - self.currentBox.getTopLeft().getY())

    def setCurrentAnnotateImage(self, annotateImage: AnnotateImage):
        self.currentAnnotateImage = annotateImage

    def finishBox(self):
        """Does the final verifications to check the validity of the currentBox,
        and either discards it or adds it to the list of boxes and the image annotations.
        A box is discarded if it covers or is covered by another box, if it intersects for more than 20%
        of its surface or the surface of the box it intersects with, if the box area is less than 40 pixels, or if
        one of its border is less than 5 pixels long."""

        if self.currentRect is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            title = "Default title"

            # Vérification de la taille minimale en pixel
            is_invalid = self.view.check_pixel_size(self.currentBox)

            if is_invalid:
                self.removeItem(self.currentRect)
                print("Box invalide (surface inférieure à 40 pixels ou largeur/longueur inférieure à 5 pixels")
            else:
                new_polygon = shapely.geometry.box(
                    min(self.currentBox.getTopLeft().getX(),
                        self.currentBox.getBottomRight().getX()),
                    min(self.currentBox.getTopLeft().getY(),
                        self.currentBox.getBottomRight().getY()),
                    max(self.currentBox.getTopLeft().getX(),
                        self.currentBox.getBottomRight().getX()),
                    max(self.currentBox.getTopLeft().getY(),
                        self.currentBox.getBottomRight().getY()))
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
                    if new_polygon.intersection(
                            current_polygon).area >= current_polygon.area * 0.2 or new_polygon.intersection(
                        current_polygon).area >= new_polygon.area * 0.2:
                        is_invalid = True
                        print("Box invalide (intersection couvrant 20% ou plus de la surface)")
                        break

            # Oui je vérifie 2 fois mais soit je suis trop bête pour le faire efficacement, soit on peut pas parce qu'on
            # change le booléen après la première vérification
            if is_invalid:
                self.removeItem(self.currentRect)
            else:
                self.currentAnnot = Annotation(None, self.currentBox)
                self.popup = PopupBox(self.currentAnnot,
                                      self.currentBox, self.box_list,
                                      self.currentRect, self.rect_list,
                                      self.currentAnnot, self.annot_list,
                                      self.main_model,
                                      self.currentAnnotateImage,
                                      self)

                self.annot_list.append(self.currentAnnot)
                self.box_list.append(self.currentBox)
                self.rect_list.append(self.currentRect)
                self.currentAnnotateImage.add_annotation(self.currentAnnot)
                self.currentRect.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    def loadAnnotations(self):
        """Loads the annotations from the current annotate image. For the scene, it means loading the list of boxes to display as rectangles"""
        self.box_list = []
        self.rect_list = []
        self.annot_list = []

        for annotation in self.currentAnnotateImage.get_annotation_list():
            self.annot_list.append(annotation)
            box = annotation.get_box()
            top_left = box.getTopLeft()
            bottom_right = box.getBottomRight()

            self.box_list.append(box)
            self.currentRect = self.addRect(top_left.getX(),
                                            top_left.getY(),
                                            abs(bottom_right.getX() - top_left.getX()),
                                            abs(top_left.getY() - bottom_right.getY()),
                                            QPen(Qt.blue))
            self.currentRect.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
            self.rect_list.append(self.currentRect)

    def set_view(self, view: View):
        self.view = view

    def getCurrentAnnotateImage(self):
        return self.currentAnnotateImage
