from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from View.main_window import MainWindow
from View.menu_bar import MenuBar
from Controller.menu_bar_controller import MenuBarController
from Controller import image_widget_controller, choose_image_area_controller


class MainController:
    main_model: ModelAnnotator
    main_view: MainWindow

    menu_bar_controller: MenuBarController

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_model = main_model
        self.main_view = main_view

        self.menu_bar_controller = MenuBarController(main_view, main_model)

        self.set_menu_bar_action(main_view.menu_bar)

    def set_menu_bar_action(self, menu_bar: MenuBar):
        menu_bar.load_image_action.triggered.connect(
            self.menu_bar_controller.load_image_menu_bar)

#    def delete_image(self, image: AnnotateImage):
#        choose_image_area_controller.delete_button(self.main_view.choose_image_area, image)
#        # si dans la graphicView la clear la graphic view
