import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, Image
from PySide6.QtCore import Slot, Qt


class ImageWidget(QtWidgets.QWidget):  # Central Widget

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = View(self.scene)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.adjustSize()

        self.setLayout(layout)


class View(QtWidgets.QGraphicsView):  # view of the image
    def mousePressEvent(self, event):
        print("QGraphicsView mousePress")

    def mouseMoveEvent(self, event):
        print("QGraphicsView mouseMove")

    def mouseReleaseEvent(self, event):
        print("QGraphicsView mouseRelease")