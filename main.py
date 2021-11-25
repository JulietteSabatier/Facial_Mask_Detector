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
        self.setFixedSize(QtCore.QSize(1280, 720))
        self.layout = QtWidgets.QVBoxLayout(self)

        self.button = QtWidgets.QPushButton("Load image")
        self.label = QtWidgets.QLabel(self)

        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.load_image)

    def load_image(self):
        self.button.hide()

        # username = getpass.getuser()

        img = str(QFileDialog.getOpenFileNames(self,
                                          "Open Image",
                                          "/users/raphael/pictures",
                                          "Image Files (*.png *.jpg *.bmp)")[0])
        lb = Label(self)
        imgPath = img[2:-2]
        lb.setPixmap(QtGui.QPixmap(imgPath))
        self.layout.addWidget(lb)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())