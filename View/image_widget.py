from PySide6 import QtWidgets

from View.custom_scene import CustomScene
from View.view import View


class ImageWidget(QtWidgets.QWidget):  # Central Widget
    scene: CustomScene
    view: View
    initialized: bool

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.initialized = False

    def initialize_scene(self):
        if not self.initialized:
            self.scene = CustomScene(self)
            self.view = View(self.scene)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.view)
            self.adjustSize()
            self.setLayout(layout)
            self.initialized = True
        else:
            self.scene.clear()
