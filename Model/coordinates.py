class Coordinates:

    def __init__(self, x, y):
        """ Create a coordinate composed by the abscissa x (float) and the ordinate y (float) """
        self.x = x
        self.y = y

    def get(self):
        """ Return the coordinate """
        return self.x, self.y

    def getX(self):
        """ Return the abscissa x of the coordinate """
        return self.x

    def getY(self):
        """ Return the ordinate y of the coordinate """
        return self.y

    def setX(self, newX):
        """ Set the abscissa x of the coordinate """
        self.x = newX

    def setY(self, newY):
        """ Set the ordinate y of the coordinate """
        self.y = newY