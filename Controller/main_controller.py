from PyQt5 import QtCore

from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from View.main_window import MainWindow
from View.menu_bar import MenuBar
from View.popup_open_project import PopupOpenProject

from Controller.menu_bar_controller import MenuBarController
from Controller.image_widget_controller import ImageWidgetController
from Controller.choose_image_area_controller import ChooseImageAreaController


class MainController:
    main_model: ModelAnnotator
    main_view: MainWindow

    menu_bar_controller: MenuBarController

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.popup_open_project = PopupOpenProject()
        self.popup_open_project.show()

        self.main_model = main_model
        self.main_view = main_view

        self.menu_bar_controller = MenuBarController(main_view, main_model)
        self.image_widget_controller = ImageWidgetController(main_view, main_model)
        self.choose_image_area_controller = ChooseImageAreaController(main_view, main_model)

        self.set_menu_bar_action()
        self.set_image_widget_action()
        self.set_choose_image_area_action()

    def set_popup_open_project_action(self):
        return 0

    def set_menu_bar_action(self):
        # Images
        self.main_view.menu_bar.load_image_action.triggered.connect(
            self.menu_bar_controller.load_image_menu_bar)

        self.main_view.menu_bar.save_images.triggered.connect(
            self.menu_bar_controller.save_images
        )

        # Categories
        self.main_view.menu_bar.import_cat.triggered.connect(
            self.menu_bar_controller.import_categories
        )

        self.main_view.menu_bar.show_all.triggered.connect(
            self.menu_bar_controller.show_categories
        )

        self.main_view.menu_bar.create_new.triggered.connect(
            self.menu_bar_controller.create_new_category
        )

        self.main_view.menu_bar.save_categories.triggered.connect(
            self.menu_bar_controller.save_categories
        )

        # Annotations
        self.main_view.menu_bar.load_annotation.triggered.connect(
            self.menu_bar_controller.load_annotations
        )

        self.main_view.menu_bar.save_annotation.triggered.connect(
            self.menu_bar_controller.save_annotations
        )

        # Project
        self.main_view.menu_bar.save_project.triggered.connect(
            self.menu_bar_controller.save_project
        )

        self.main_view.menu_bar.load_project.triggered.connect(
            self.menu_bar_controller.load_project
        )

        self.main_view.menu_bar.create_project.triggered.connect(
            self.menu_bar_controller.create_project
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


