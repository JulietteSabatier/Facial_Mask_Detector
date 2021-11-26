import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, Image


class ImageAnnotator(QtWidgets.QMainWindow):  # main window
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.Widget()

    def Widget(self):
        self.w = Widget()
        self.setCentralWidget(self.w)


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = View(self.scene)
        self.button = QtWidgets.QPushButton("load image")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.button.clicked.connect(self.load_image)

    def load_image(self):
        self.scene.clear()
        img = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                     "Open Image",
                                                     "/users/yannb/pictures",
                                                     "Image Files (*.png *.jpg *.bmp)")[0]
        imgPath = img[0]
        image = Image.open(imgPath)
        w, h = image.size
        self.imgQ = ImageQt.ImageQt(image)  # we need to hold reference to imgQ
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.scene.update()


class View(QtWidgets.QGraphicsView):
    def mousePressEvent(self, event):
        print("QGraphicsView mousePress")

    def mouseMoveEvent(self, event):
        print("QGraphicsView mouseMove")

    def mouseReleaseEvent(self, event):
        print("QGraphicsView mouseRelease")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    imageAnnotator = ImageAnnotator()
    imageAnnotator.resize(640, 480)
    imageAnnotator.show()
    sys.exit(app.exec())