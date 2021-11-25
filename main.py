import getpass
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog


# https://stackoverflow.com/a/44508342
class Label(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.p = QtGui.QPixmap()

    def setPixmap(self, p):
        self.p = p
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        # self.setFixedSize(QtCore.QSize(1280, 720))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("Facial Mask Detector")

        self.button = QtWidgets.QPushButton("Load image")
        self.label = QtWidgets.QLabel(self)

        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.load_image)

    def load_image(self):

        basePath = "/users/" + getpass.getuser() + "/pictures"
        img = QFileDialog.getOpenFileNames(self,
                                          "Open Image",
                                          basePath,
                                          "Image Files (*.png *.jpg *.bmp)")[0]
        if len(img) > 0:
            self.button.hide() #on peut toujours cliquer sur le bouton si on a pas ouvert d'image
            for imgPath in img:
                label = QtWidgets.QLabel(pixmap = QtGui.QPixmap(imgPath))
                self.layout.addWidget(label)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())