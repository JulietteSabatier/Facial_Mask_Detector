from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Qt


class ChooseImageArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        QtWidgets.QScrollArea.__init__(self, parent)
        self.widget = QtWidgets.QWidget()
        self.box = QtWidgets.QVBoxLayout()
        self.box.addStretch(-1)
        self.widget.setLayout(self.box)


        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)
        self.setMaximumWidth(150)

    @Slot()
    def add_image(self, img):
        button = QtWidgets.QPushButton(img.split("/")[-1].split(".")[0])
        button.path = img
        # Adjust size of the text in the button
        # Adjust size of the button in the area
        self.box.addWidget(button)

    @Slot()
    def delete_image(self):
        print("Delete image in the Scroll Area")
