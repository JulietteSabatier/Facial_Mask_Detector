from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QGraphicsRectItem

from Model.Coordinates import Coordinates


class Box(QtWidgets.QGraphicsRectItem):
    topLeft: Coordinates
    bottomRight: Coordinates
    width: float
    height: float
    box: QGraphicsRectItem

    def __init__(self, scene, x, y):
        super().__init__()
        self.topLeft = Coordinates(x, y)
        self.bottomRight = Coordinates(x, y)
        self.width = 0
        self.height = 0
        self.scene = scene
        self.setPen(QPen(Qt.blue))
        self.box = self.scene.addRect(x, y, self.bottomRight.getX() - self.topLeft.getX(), self.bottomRight.getY() - self.topLeft.getY(), QPen(Qt.blue))


    def update(self):
        self.width = self.bottomRight.getX() - self.topLeft.getX()
        self.height = self.bottomRight.getY() - self.topLeft.getY()

        self.box.setRect(self.topLeft.getX(),
                     self.topLeft.getY(),
                     self.width,
                     self.height)


    def updateTopLeft(self, newX, newY):
        self.topLeft.setX(newX)
        self.topLeft.setY(newY)

    def updateBottomRight(self, newX, newY):
        self.bottomRight.setX(newX)
        self.bottomRight.setY(newY)

    def getBox(self):
        return self.box

    def getTopLeft(self):
        return self.topLeft

    def getBottomRight(self):
        return self.bottomRight

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
