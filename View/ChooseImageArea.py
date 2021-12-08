from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class MyButton(QtWidgets.QPushButton):

    def __init__(self, name):
        super(MyButton, self).__init__()
        self.setText(name)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setToolTip(name)

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
        button = MyButton(img_title)
        list_widget = QtWidgets.QListWidget()
        list_widget.addItem(button.text())
        self.insertItem(1, button.text())

    def delete_image(self):
        print("Delete image in the Scroll Area")
