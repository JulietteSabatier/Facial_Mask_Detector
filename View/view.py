from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class View(QtWidgets.QGraphicsView):  # view of the image
    def __init__(self, scene):
        QtWidgets.QGraphicsView.__init__(self, scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = scene
