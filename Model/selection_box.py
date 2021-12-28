
from Model.coordinates import Coordinates


class Box:
    topLeft: Coordinates
    bottomRight: Coordinates
    width: float
    height: float

    def __init__(self, x, y):
        """ Create a box composed by two Coordinate topLeft and bottomRight """
        self.topLeft = Coordinates(x, y)
        self.bottomRight = Coordinates(x, y)
        self.width = 0
        self.height = 0

    def update(self):
        """ Update the width and the height of the box, calculating with it coordinate """
        self.width = self.bottomRight.getX() - self.topLeft.getX()
        self.height = self.bottomRight.getY() - self.topLeft.getY()

    def updateTopLeft(self, newX, newY):
        """ Update the topLeft point of the box with a new abscissa x and a new ordinate y"""
        self.topLeft.setX(newX)
        self.topLeft.setY(newY)

    def updateBottomRight(self, newX, newY):
        """ Update the bottomRight point of the box with a new abscissa x and a new ordinate y"""
        self.bottomRight.setX(newX)
        self.bottomRight.setY(newY)

    def get_position_as_json(self):
        """ Return the position convert in a json format """
        return {"top_left": {
                    "abs": self.getTopLeft().getX(),
                    "ord": self.getTopLeft().getY()},

                "bottom_right": {
                    "abs": self.getBottomRight().getX(),
                    "ord": self.getBottomRight().getY()}
                }

    def getTopLeft(self):
        """ Return the coordinate of the topLeft point of the box"""
        return self.topLeft

    def getBottomRight(self):
        """ Return the coordinate of the bottomRight point of the box """
        return self.bottomRight

    def getWidth(self):
        """ Return the width of the box"""
        return self.width

    def getHeight(self):
        """ Return the height of the box"""
        return self.height
