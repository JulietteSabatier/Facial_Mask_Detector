import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, Image
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QPushButton


class MyButton(QPushButton):

    def __init__(self, name):
        super(MyButton, self).__init__()
        self.setText(name)
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
        #self.setWidgetResizable(True)
        #self.setWidget(self.widget)
        self.setFixedWidth(150)

    @Slot()
    def add_image(self, img_title: str):

        button = QtWidgets.QListWidgetItem(img_title, self)
        self.insertItem(1, button)



    @Slot()
    def delete_image(self):
        print("Delete image in the Scroll Area")
