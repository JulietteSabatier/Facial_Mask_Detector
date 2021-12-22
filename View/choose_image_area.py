import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Slot, Qt
from Model.model_annotator import ModelAnnotator


# Créer le visuel de la scroll bar des nom des images

class MyButton(QtWidgets.QListWidgetItem):
    main_model: ModelAnnotator

    # Pas encore fini
    def __init__(self, name):
        super(MyButton, self).__init__()
        inside_button = QtWidgets.QPushButton()
        self.setText(name)
        self.setToolTip(name)


class ChooseImageArea(QtWidgets.QListWidget):
    def __init__(self, main_model: ModelAnnotator):
        QtWidgets.QListWidget.__init__(self)

        self.main_model = main_model

        self.widget = QtWidgets.QWidget()
        self.box = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.box)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedWidth(150)

        self.remove_action = QtGui.QAction("Delete")
        self.rename_action = QtGui.QAction("Rename")
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.remove_action)
        self.addAction(self.rename_action)

    def load_all_images(self):
        for image in self.main_model.image_list:
            self.add_image(image.title)

    def add_image(self, img_title: str):
        widget_item = QtWidgets.QListWidgetItem(img_title)
        self.insertItem(1, widget_item)

    def delete_image(self):
        item_image = self.takeItem(self.row(self.currentItem()))
        name_image = item_image.text()
        return name_image

    def rename_image_input(self):
        text, result = QtWidgets.QInputDialog.getText(self, "Rename ", "New name of the image: ")
        if result:
            self.currentItem().setText(text)
            return text
