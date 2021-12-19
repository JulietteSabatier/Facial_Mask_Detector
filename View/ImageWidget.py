from PySide6 import QtWidgets

from View.CustomScene import CustomScene
from View.View import View


class ImageWidget(QtWidgets.QWidget):  # Central Widget
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = CustomScene(self)
        self.view = View(self.scene)
        self.parent = parent
