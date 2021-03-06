from Model.annotate_image import AnnotateImage
from Model.annotation import Annotation
from Model.model_annotator import ModelAnnotator
from Model.selection_box import Box
from PySide6 import QtGui, QtWidgets


class PopupBox(QtWidgets.QDialog):
    annotation: Annotation
    box: Box
    main_model: ModelAnnotator
    image: AnnotateImage
    rect: QtWidgets.QGraphicsRectItem

    def __init__(self, annotation: Annotation,
                 box: Box, box_list: list[Box],
                 rect: QtWidgets.QGraphicsRectItem, rect_list: list[QtWidgets.QGraphicsRectItem],
                 annot: Annotation, annot_list: list[Annotation],
                 main_model: ModelAnnotator,
                 image: AnnotateImage,
                 scene: QtWidgets.QGraphicsScene):

        super(PopupBox, self).__init__()
        icon = QtGui.QIcon("iconMask.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("Annotation Information")

        self.current_box = box
        self.annotation = annotation
        self.main_model = main_model
        self.image = image
        self.current_rect = rect
        self.rect_list = rect_list
        self.box_list = box_list
        self.current_annot = annot
        self.annot_list = annot_list
        self.scene = scene

        self.resize(400, 200)

        # Print position
        self.widget_position_box = QtWidgets.QWidget()
        self.widget_position_box_layout = QtWidgets.QVBoxLayout()
        self.widget_position_box.setLayout(self.widget_position_box_layout)
        self.widget_position_box_layout.addWidget(QtWidgets.QLabel("Left Up Point:\n"
                                                                   + "x: " + str(box.getTopLeft().getX())
                                                                   + "\n"
                                                                   + "y: " + str(box.getTopLeft().getY())))
        self.widget_position_box_layout.addWidget(QtWidgets.QLabel("Bottom Right Point: \n"
                                                                   + "x: " + str(box.getBottomRight().getX())
                                                                   + "\n"
                                                                   + "y: " + str(box.getBottomRight().getY())))

        self.combo_box = QtWidgets.QComboBox()
        for category in self.main_model.category_list:
            self.combo_box.addItem(category.name)
        if annotation.title is not None:
            self.widget_position_box_layout.addWidget(QtWidgets.QLabel("Category: " + str(annotation.title.name)))
        else:
            self.widget_position_box_layout.addWidget(QtWidgets.QLabel("No chosen category"))
        self.widget_position_box_layout.addWidget(QtWidgets.QLabel("Choose a new category below: "))
        self.widget_position_box_layout.addWidget(
            self.combo_box)

        self.button_save = QtWidgets.QPushButton("Save")
        self.button_delete = QtWidgets.QPushButton("Delete")

        self.central_box = QtWidgets.QVBoxLayout()
        self.central_box.addWidget(self.widget_position_box)
        self.central_box.addWidget(self.button_save)
        self.central_box.addWidget(self.button_delete)
        self.setLayout(self.central_box)

        self.button_delete.clicked.connect(self.delete_action)
        self.button_save.clicked.connect(self.save_action)
        self.exec()

    def save_action(self):
        name_cat = self.combo_box.currentText()
        category = self.main_model.get_category_by_name(name_cat)
        self.annotation.title = category
        self.close()

    def delete_action(self):
        self.image.remove_annotation(self.current_box)
        self.scene.removeItem(self.current_rect)
        self.box_list.remove(self.current_box)
        self.current_box = None
        self.rect_list.remove(self.current_rect)
        self.current_rect = None
        self.annot_list.remove(self.current_annot)
        self.current_annot = None
        self.close()
