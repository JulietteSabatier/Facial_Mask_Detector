from Model.model_annotator import ModelAnnotator
from Model.selection_box import Box
from Model.annotation import Annotation
from View.popup_box import PopupBox

from PySide6 import QtWidgets

# Non utilisé pour porblème de signaux suite a celui du custom scene controller

class PopupBoxController:
    popup_box: PopupBox
    main_model: ModelAnnotator

    def __init__(self, popup_box: PopupBox,
                 main_model: ModelAnnotator,
                 scene: QtWidgets.QGraphicsScene,
                 box_list: list[Box], current_box: Box,
                 rect_list: list[QtWidgets.QGraphicsRectItem], current_rect: QtWidgets.QGraphicsRectItem,
                 annot_list: list[Annotation], current_annot: Annotation):

        self.popup_box = popup_box
        self.scene = scene
        self.main_model = main_model
        self.box_list = box_list
        self.rect_list = rect_list
        self.annot_list = annot_list
        self.current_annot = current_annot
        self.current_box = current_box
        self.current_rect = current_rect

        #self.popup_box.button_save.clicked.connect(self.save_action)
        #self.popup_box.button_delete.clicked.connect(self.delete_action)

    def save_action(self):
        print("save action popup")
        name_cat = self.popup_box.combo_box.currentText()
        category = self.main_model.get_category_by_name(name_cat)
        self.popup_box.annotation.title = category
        self.popup_box.close()

    def delete_action(self):
        print("delete action popup")
        self.popup_box.image.remove_annotation(self.popup_box.box)
        #self.custom_scene.removeItem(self.popup_box.rect)
        self.scene.removeItem(self.popup_box.rect)
        #self.custom_scene.box_list.remove(self.custom_scene.currentBox)
        self.box_list.remove(self.current_box)
        #self.custom_scene.currentBox = None
        self.current_box = None
        #self.custom_scene.rect_list.remove(self.custom_scene.currentRect)
        self.rect_list.remove(self.current_rect)
        #self.custom_scene.currentRect = None
        self.current_rect = None
        #self.custom_scene.annot_list.remove(self.custom_scene.currentAnnot)
        self.annot_list.remove(self.current_annot)
        #self.custom_scene.currentAnnot = None
        self.current_annot = None
        self.popup_box.close()


