import os.path
import sys

from PySide6 import QtWidgets

from Controller.main_controller import MainController
from Model.model_annotator import ModelAnnotator
from View.main_window import MainWindow

if __name__ == '__main__':  # main
    app = QtWidgets.QApplication(sys.argv)

    list_image = []
    list_category = []

    if not os.path.exists("Project"):
        os.mkdir("Project")
    model_annotator = ModelAnnotator(list_category, list_image)
    main_window = MainWindow(model_annotator)
    main_controller = MainController(model_annotator, main_window)
    sys.exit(app.exec())
