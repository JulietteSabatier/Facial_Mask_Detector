import sys
from PySide6 import QtCore, QtWidgets, QtGui


class ImageAnnotator(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.baseSize()
        self.windowTitle()
        self.setWindowTitle("Image Annotator")
        icon = QtGui.QIcon("iconMask.png")
        self.setWindowIcon(icon)
        self.resize(800, 600)
        self.create_menu_bar()
        self.create_scroll_area()
        self.show()

    def create_menu_bar(self):
        menu_bar = QtWidgets.QMenuBar(self)
        menu_bar.addMenu("Load Image")
        menu_bar.addMenu("Import Categories")
        menu_bar.addMenu("Save Annotations")
        self.setMenuBar(menu_bar)

    def create_scroll_area(self):
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ImageAnnotator()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
