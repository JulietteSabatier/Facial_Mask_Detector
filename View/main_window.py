from Model.model_annotator import ModelAnnotator
from PySide6 import QtGui, QtWidgets

from View.choose_image_area import ChooseImageArea
from View.image_widget import ImageWidget
from View.menu_bar import MenuBar
from View.popup_open_project import PopupOpenProject

# Créer la main Window

class MainWindow(QtWidgets.QMainWindow):  # main window
    model_annotator: ModelAnnotator

    def __init__(self, model_annotator: ModelAnnotator):
        super(MainWindow, self).__init__()
        self.model_annotator = model_annotator

        self.image_widget = ImageWidget(model_annotator)
        self.choose_image_area: ChooseImageArea = ChooseImageArea(model_annotator)
        self.menu_bar = MenuBar()

        self.popup_open_project = PopupOpenProject()

        # Main Widget and layout
        page_layout = QtWidgets.QHBoxLayout()
        page_layout.addWidget(self.choose_image_area)
        page_layout.addWidget(self.image_widget)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(page_layout)

        # Set widget
        self.setCentralWidget(central_widget)
        self.setMenuBar(self.menu_bar)

        self.init_ui()
        self.show()
        self.popup_open_project.show()

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
        return self.choose_image_area

    def get_image_widget(self):
        return self.image_widget

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowIcon(QtGui.QIcon("iconMask.png"))
        message_box.setText("You may have unsaved changes, are you sure you want to close the application ?")
        message_box.addButton(QtWidgets.QMessageBox.Cancel)
        message_box.addButton(QtWidgets.QMessageBox.Close)
        result = message_box.exec()
        if result == QtWidgets.QMessageBox.Close:
            event.accept()
        if result == QtWidgets.QMessageBox.Cancel:
            event.ignore()
