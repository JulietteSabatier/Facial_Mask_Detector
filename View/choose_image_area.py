import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, Image
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QPushButton


# Créer le visuel de la scroll bar des nom des images

class MyButton(QtWidgets.QPushButton):
    # Pas encore fini
    def __init__(self, name):
        super(MyButton, self).__init__()
        inside_button = QtWidgets.QPushButton()
        self.setText(name)
        self.setToolTip(name)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(QAction("delete", self))
        self.show()


class ChooseImageArea(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)

        self.widget = QtWidgets.QWidget()
        self.box = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.box)



        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedWidth(150)

    def add_image(self, img_title: str):
        #button = MyButton(img_title)
        widget_item = QtWidgets.QListWidgetItem(img_title)

        #self.setItemWidget(widget_item, button)
        self.insertItem(1, widget_item)

    def delete_image(self):
        print("Delete image in the Scroll Area")
