import shapely.geometry
from Model.annotation import Annotation
from Model.model_annotator import ModelAnnotator
from Model.selection_box import Box
from Model.annotation import Annotation

from PySide6 import QtCore, QtGui, QtWidgets
from Controller.popup_box_controller import PopupBoxController

# Unused for now from signal problem
class CustomSceneController:

    main_model: ModelAnnotator

    def __init__(self, main_model: ModelAnnotator):
        """ Define the functions which permit to update the choose_image_area
                which contains the names of the annotates image"""
        self.main_model = main_model
        self.custom_scene = custom_scene

    def mouse_press_event_action(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """ Function which create a new box and rectangle in the given scene"""
        # Left click = creating a new box
        if event.button() == QtCore.Qt.LeftButton:
            if self.custom_scene.currentRect is not None:
                self.custom_scene.currentRect.setSelected(False)

            self.custom_scene.currentBox = Box(event.scenePos().x(), event.scenePos().y())
            self.custom_scene.currentRect = self.custom_scene.addRect(event.scenePos().x(),
                                                                      event.scenePos().y(),
                                                                      0, 0,
                                                                      QtGui.QPen(QtCore.Qt.blue))
            self.custom_scene.left_click_pressed = True

    def mouse_move_event_action(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """ Function which update the box and rectangle in the given scene when the pressed mouse (left clicked)
          move"""
        # If the left click is pressed (we must not do it with right click), we update the box we're creating
        if self.custom_scene.left_click_pressed:
            self.custom_scene.currentRect.updateRect(event.scenePos().x(), event.scenePos().y())

    def mouse_release_event_action(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """ Function which create the annotation of the rectangle given by the scene when the mousse is released.
        Use the function finishBox() in order to verify if the box is valid"""
        # If it's the left click (we don't care about the right click), we update the box one last time
        # and then call the function to check its final validity
        if event.button() == QtCore.Qt.LeftButton \
                and self.custom_scene.currentRect is not None \
                and not self.custom_scene.currentRect.isSelected():
            self.custom_scene.currentRect.updateRect(event.scenePos().x(), event.scenePos().y())
            self.custom_scene.currentBox.updateBottomRight(event.scenePos().x(), event.scenePos().y())
            self.custom_scene.currentBox.update()
            self.finishBox()
            self.custom_scene.left_click_pressed = False

    def mouse_double_click_event_action(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """ Function which permit to modify the category or delete an annotation which is around the position of the
        double click on the given scene."""
        if event.button() == QtCore.Qt.LeftButton:
            for rect in self.custom_scene.rect_list:
                if rect.contains(event.scenePos()):
                    rect.setSelected(True)
                    self.custom_scene.currentRect = rect
                    index = self.custom_scene.rect_list.index(self.custom_scene.currentRect)
                    self.custom_scene.currentBox = self.custom_scene.box_list.__getitem__(index)
                    self.custom_scene.currentAnnot = self.custom_scene.annot_list.__getitem__(index)
                    popup = PopupBox(self.custom_scene.currentAnnot,
                                     self.custom_scene.currentBox,
                                     self.custom_scene.currentRect,
                                     self.main_model,
                                     self.custom_scene.currentAnnotateImage)
                    popup_controller = PopupBoxController(popup, self.custom_scene, self.main_model)
                    print("double click on annot0, ", self.custom_scene.currentAnnot.title)
                    break

    def updateRect(self, x, y):
        """ Function which update the coordinates of the current box and rectangle """
        self.custom_scene.currentBox.update()
        self.custom_scene.currentRect.setRect(
            self.custom_scene.currentBox.getTopLeft().getX(),
            self.custom_scene.currentBox.getTopLeft().getY(),
            x - self.custom_scene.currentBox.getTopLeft().getX(),
            y - self.custom_scene.currentBox.getTopLeft().getY())

    def finishBox(self):
        """Does the final verifications to check the validity of the currentBox,
        and either discards it or adds it to the list of boxes and the image annotations.
        A box is discarded if it covers or is covered by another box, if it intersects for more than 20%
        of its surface or the surface of the box it intersects with, if the box area is less than 40 pixels, or if
        one of its border is less than 5 pixels long."""

        if self.custom_scene.currentRect is not None:
            # Le mieux serait de faire un pop-up qui permette de donner un titre
            title = "Default title"

            # Vérification de la taille minimale en pixel
            is_invalid = self.custom_scene.view.check_pixel_size(self.custom_scene.currentBox)

            if is_invalid:
                self.custom_scene.removeItem(self.custom_scene.currentRect)
                print("Box invalide (surface inférieure à 40 pixels ou largeur/longueur inférieure à 5 pixels")
            else:
                new_polygon = shapely.geometry.box(
                    min(self.custom_scene.currentBox.getTopLeft().getX(),
                        self.custom_scene.currentBox.getBottomRight().getX()),
                    min(self.custom_scene.currentBox.getTopLeft().getY(),
                        self.custom_scene.currentBox.getBottomRight().getY()),
                    max(self.custom_scene.currentBox.getTopLeft().getX(),
                        self.custom_scene.currentBox.getBottomRight().getX()),
                    max(self.custom_scene.currentBox.getTopLeft().getY(),
                        self.custom_scene.currentBox.getBottomRight().getY()))
                for box in self.custom_scene.box_list:
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
                self.custom_scene.removeItem(self.custom_scene.currentRect)
            else:
                self.custom_scene.currentAnnot = Annotation(None, self.custom_scene.currentBox)
                popup = PopupBox(self.custom_scene.currentAnnot,
                                 self.custom_scene.currentBox,
                                 self.custom_scene.currentRect,
                                 self.main_model,
                                 self.custom_scene.currentAnnotateImage)

                self.custom_scene.annot_list.append(self.custom_scene.currentAnnot)
                self.custom_scene.box_list.append(self.custom_scene.currentBox)
                self.custom_scene.rect_list.append(self.custom_scene.currentRect)
                self.custom_scene.currentAnnotateImage.add_annotation(self.custom_scene.currentAnnot)
                self.custom_scene.currentRect.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
