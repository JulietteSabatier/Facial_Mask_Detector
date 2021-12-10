from PyQt5 import QtCore

from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from View.main_window import MainWindow
from View.menu_bar import MenuBar

from Controller.menu_bar_controller import MenuBarController
from Controller.image_widget_controller import ImageWidgetController
from Controller.choose_image_area_controller import ChooseImageAreaController


class MainController:
    main_model: ModelAnnotator
    main_view: MainWindow

    menu_bar_controller: MenuBarController

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_model = main_model
        self.main_view = main_view

        self.menu_bar_controller = MenuBarController(main_view, main_model)
        self.image_widget_controller = ImageWidgetController(main_view, main_model)
        self.choose_image_area_controller = ChooseImageAreaController(main_view, main_model)

        self.set_menu_bar_action()
        self.set_image_widget_action()
        self.set_choose_image_area_action()

    def set_menu_bar_action(self):
        # Load image
        self.main_view.menu_bar.load_image_action.triggered.connect(
            self.menu_bar_controller.load_image_menu_bar)

        # Import categories from csv
        self.main_view.menu_bar.import_csv.triggered.connect(
            self.menu_bar_controller.import_categories_from_csv
        )

        # Import categories from json
        self.main_view.menu_bar.import_json.triggered.connect(
            self.menu_bar_controller.import_categories_from_json
        )

    def set_image_widget_action(self):
        return 0

    def set_choose_image_area_action(self):
        # Double Click on the name : load in the graphic scene
        self.main_view.choose_image_area.doubleClicked.connect(lambda:
                                                self.image_widget_controller.load_image_widget(
                                                       self.main_model.get_image_by_name(
                                                           self.main_view.choose_image_area.currentItem().text())))
        # Context menu : delete image
        self.main_view.choose_image_area.remove_action.triggered.connect(
                    self.choose_image_area_controller.delete_button
        )

        # Context menu : rename image
        self.main_view.choose_image_area.rename_action.triggered.connect(
            self.choose_image_area_controller.rename_button
        )


