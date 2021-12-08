import sys

import View.MainWindow
import Model.ModelAnnotator as ModelAnnotator
import Controller.MainController as MainController
from PySide6 import QtWidgets


if __name__ == '__main__':  # main
    app = QtWidgets.QApplication(sys.argv)

    list_image = []
    list_category = []
    model_annotator = ModelAnnotator.ModelAnnotator(list_category, list_image)
    main_window = View.MainWindow.ImageAnnotator(model_annotator)
    main_controller = MainController.MainController(model_annotator, main_window)

    sys.exit(app.exec())
