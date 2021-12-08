from PySide6.QtGui import QPen, Qt
from PySide6.QtWidgets import QGraphicsItem

class Box:
    def __init__(self, scene, x, y):
        self.topLeft = Coordinates(x, y)
        self.bottomRight = Coordinates(x, y)
        self.width = 0
        self.height = 0
        self.scene = scene
        self.box = self.scene.addRect(x, y, self.bottomRight.getX() - self.topLeft.getX(), self.bottomRight.getY() - self.topLeft.getY(), QPen(Qt.blue))
        # self.box.setFlag(QGraphicsItem.ItemIsMovable)


    def update(self, eventPosX, eventPosY):
        self.updateBottomRight(eventPosX, eventPosY)

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


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, newX):
        self.x = newX

    def setY(self, newY):
        self.y = newY