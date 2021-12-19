from PySide6 import QtWidgets

from View.custom_scene import CustomScene
from View.view import View


class ImageWidget(QtWidgets.QWidget):  # Central Widget
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = CustomScene(self)
        self.view = View(self.scene)
        self.parent = parent
