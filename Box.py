

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, newX, newY):
        self.setX(newX)
        self.setY(newY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, newX):
        self.x = newX

    def setY(self, newY):
        self.y = newY