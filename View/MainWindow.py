from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Slot

import View.MenuBar
from View import ChooseImageArea, ImageWidget
from Model import ModelAnnotator


class ImageAnnotator(QtWidgets.QMainWindow):  # main window
    model_annotator: ModelAnnotator

    def __init__(self, model_annotator: ModelAnnotator):
        super().__init__()
        self.model_annotator = model_annotator

        self.w = ImageWidget.ImageWidget()
        self.c = ChooseImageArea.ChooseImageArea()
        self.menu_bar = View.MenuBar.MenuBar()

        # Main Widget and layout
        page_layout = QtWidgets.QHBoxLayout()
        page_layout.addWidget(self.c)
        page_layout.addWidget(self.w)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(page_layout)

        # Set widget
        self.setCentralWidget(central_widget)
        self.setMenuBar(self.menu_bar)

        self.init_ui()
        self.show()

    def init_ui(self):
        self.baseSize()
        self.windowTitle()
        self.setWindowTitle("Image Annotator")
        icon = QtGui.QIcon("iconMask.png")
        self.setWindowIcon(icon)
        self.resize(1000, 600)

    def get_model_annotator(self):
        return self.model_annotator

    def get_choose_image_area(self):
        return self.c

    def get_image_widget(self):
        return self.w

