import sys

from View.main_window import MainWindow
from Model.model_annotator import ModelAnnotator
from Controller.main_controller import MainController
from PySide6 import QtWidgets


if __name__ == '__main__':  # main
    app = QtWidgets.QApplication(sys.argv)

    list_image = []
    list_category = []
    model_annotator = ModelAnnotator(list_category, list_image)
    main_window = MainWindow(model_annotator)
    main_controller = MainController(model_annotator, main_window)

    sys.exit(app.exec())
