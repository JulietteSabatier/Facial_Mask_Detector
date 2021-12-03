from Model import ModelAnnotator
from View import MainWindow
from Controller import MenuBarController


class MainController:
    main_model: ModelAnnotator
    main_view: MainWindow

    menu_bar_controller: MenuBarController

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_model = main_model
        self.main_view = main_view

        self.menu_bar_controller = MenuBarController.MenuBarController(main_model, main_view)

        self.set_menu_bar_action()

    def set_menu_bar_action(self):
        self.main_view.menu_bar.image.load_image.triggered.connect(self.menu_bar_controller.load_image_function)
