from PIL import ImageQt, Image
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Slot

import Box


class ImageWidget(QtWidgets.QWidget):  # Central Widget

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = View(self.scene)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.adjustSize()
        self.setLayout(layout)

    @Slot()
    def load_image(self, img):
        if len(img) > 0:
            self.scene.clear()
            imgPath = img[0]
            image = Image.open(imgPath)
            w, h = image.size
            self.imgQ = ImageQt.ImageQt(image)  # we need to hold reference to imgQ
            pixMap = QtGui.QPixmap.fromImage(self.imgQ)
            self.scene.addPixmap(pixMap)
            self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.scene.update()


class View(QtWidgets.QGraphicsView):  # view of the image
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.startCurrentBox = Box.Coordinates(0, 0)
        self.endCurrentBox = Box.Coordinates(0, 0)
        self.scene = parent
        self.currentBox = self.scene.addRect(0, 0, 0, 0)



    def mousePressEvent(self, event):
        print("QGraphicsView mousePress")

        self.startCurrentBox.update(event.x(), event.y())
        self.endCurrentBox.update(event.x(), event.y())
        self.currentBox = self.scene.addRect(self.startCurrentBox.getX(),
                                         self.startCurrentBox.getY(),
                                         self.endCurrentBox.getX(),
                                         self.endCurrentBox.getY())

        print(self.startCurrentBox.getX(), self.startCurrentBox.getY())

    def mouseMoveEvent(self, event):
        self.updateCurrentBox(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        print("QGraphicsView mouseRelease")

        self.updateCurrentBox(event.x(), event.y())
        print(self.endCurrentBox.getX(), self.endCurrentBox.getY())

        self.startCurrentBox.setX(0)
        self.startCurrentBox.setY(0)
        self.endCurrentBox.setX(0)
        self.endCurrentBox.setY(0)

    def updateCurrentBox(self, eventPosX, eventPosY):
        self.endCurrentBox.update(eventPosX, eventPosY)

        width = self.endCurrentBox.getX() - self.startCurrentBox.getX()
        height = self.endCurrentBox.getY() - self.startCurrentBox.getY()

        print("width = ", width, ", height = " , height)

        self.currentBox.setRect(self.startCurrentBox.getX(),
                                self.startCurrentBox.getY(),
                                width,
                                height)
