from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QGraphicsRectItem

from Model.coordinates import Coordinates


class Box:
    topLeft: Coordinates
    bottomRight: Coordinates
    width: float
    height: float
    #box: QGraphicsRectItem

    def __init__(self, scene, x, y):
        self.topLeft = Coordinates(x, y)
        self.bottomRight = Coordinates(x, y)
        self.width = 0
        self.height = 0
        #self.scene = scene
        #self.box = self.scene.addRect(x, y, 0, 0, QPen(Qt.blue))


    def update(self):
        self.width = self.bottomRight.getX() - self.topLeft.getX()
        self.height = self.bottomRight.getY() - self.topLeft.getY()

        #self.box.setRect(self.topLeft.getX(),
        #             self.topLeft.getY(),
        #             self.width,
        #             self.height)


    def updateTopLeft(self, newX, newY):
        self.topLeft.setX(newX)
        self.topLeft.setY(newY)

    def updateBottomRight(self, newX, newY):
        self.bottomRight.setX(newX)
        self.bottomRight.setY(newY)

    def get_position_as_json(self):
        return {"top_left": {
                    "abs": self.getTopLeft().getX(),
                    "ord": self.getTopLeft().getY()},

                "bottom_right": {
                    "abs": self.getBottomRight().getX(),
                    "ord": self.getBottomRight().getY()}
                }

    def setBox(self, newBox: QGraphicsRectItem):
        self.box = newBox

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
