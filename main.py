import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, Image
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction


class ImageAnnotator(QtWidgets.QMainWindow):  # main window
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.w = Widget()
        self.c = ChooseImageArea()
        self.init_ui()
        self.Widget()
        self.ChooseImageArea()

        # Scroll area

    def Widget(self):  # Central widget
        self.setCentralWidget(self.w)

    def ChooseImageArea(self):
        pass

    def init_ui(self):
        self.baseSize()
        self.windowTitle()
        self.setWindowTitle("Image Annotator")
        icon = QtGui.QIcon("iconMask.png")
        self.setWindowIcon(icon)
        self.resize(800, 600)
        self.create_menu_bar()
        self.show()

    def create_menu_bar(self):
        menu_bar = QtWidgets.QMenuBar(self)

        # Images
        image = QtWidgets.QMenu("Image", menu_bar)

        # Load image
        load_image = QtGui.QAction("Load Image", image)
        image.addAction(load_image)
        load_image.triggered.connect(self.w.load_image)

        # Delete Image
        delete_image = QtGui.QAction("Delete Image", image)
        image.addAction(delete_image)
        # delete_image.triggered.connect(slot_to_delete_an_image)

        # Import Categories
        import_cat = QtWidgets.QMenu("Import Categories", menu_bar)

        # Import from csv
        import_csv = QtGui.QAction("From cvs", import_cat)
        import_cat.addAction(import_csv)
        # import_csv.triggered.connect(slot_to_import_categories_from_cvs)

        # Import from json
        import_json = QtGui.QAction("From json", import_cat)
        import_cat.addAction(import_json)
        # import_json.triggered.connect(slot_to_import_categories_from_json)

        # Save
        save = QtWidgets.QMenu("Save", menu_bar)

        # Save Categories
        save.save_categories = QtGui.QAction("Save Categories", save)
        save.addAction(save.save_categories)
        # save_categories.triggered.connect(slot_to_save_categories)

        # Add to menuBar
        menu_bar.addMenu(image)
        menu_bar.addMenu(import_cat)
        menu_bar.addMenu(save)

        # Define menuBar
        self.setMenuBar(menu_bar)


class Widget(QtWidgets.QWidget):  # Central Widget
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = View(self.scene)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    @Slot()
    def load_image(self):
        self.scene.clear()
        img = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                     "Open Image",
                                                     "/users/julie/pictures",
                                                     "Image Files (*.png *.jpg *.bmp)")[0]
        if len(img) != 0:
            imgPath = img[0]
            image = Image.open(imgPath)
            w, h = image.size
            self.imgQ = ImageQt.ImageQt(image)  # we need to hold reference to imgQ
            pixMap = QtGui.QPixmap.fromImage(self.imgQ)
            self.scene.addPixmap(pixMap)
            self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            self.scene.update()


class ChooseImageArea(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.scene = QtWidgets.QScrollArea()

        def add_image():
            return None

        def delete_image():
            return None


class View(QtWidgets.QGraphicsView):  # view of the image
    def mousePressEvent(self, event):
        print("QGraphicsView mousePress")

    def mouseMoveEvent(self, event):
        print("QGraphicsView mouseMove")

    def mouseReleaseEvent(self, event):
        print("QGraphicsView mouseRelease")


if __name__ == '__main__':  # main
    app = QtWidgets.QApplication(sys.argv)
    imageAnnotator = ImageAnnotator()
    imageAnnotator.resize(640, 480)
    imageAnnotator.show()
    sys.exit(app.exec())
