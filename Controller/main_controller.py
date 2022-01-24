from Model.model_annotator import ModelAnnotator
from View.main_window import MainWindow

from Controller.choose_image_area_controller import ChooseImageAreaController
from Controller.image_widget_controller import ImageWidgetController
from Controller.menu_bar_controller import MenuBarController
from Controller.popup_open_project_controller import PopupOpenProjectController


class MainController:
    main_model: ModelAnnotator
    main_view: MainWindow

    project_name: str

    menu_bar_controller: MenuBarController
    image_widget_controller: ImageWidgetController
    choose_image_area_controller: ChooseImageAreaController
    popup_open_project_controller: PopupOpenProjectController

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):

        self.main_model = main_model
        self.main_view = main_view

        self.menu_bar_controller = MenuBarController(main_view, main_model)
        self.image_widget_controller = ImageWidgetController(main_view, main_model)
        self.choose_image_area_controller = ChooseImageAreaController(main_view, main_model)
        self.popup_open_project_controller = PopupOpenProjectController(main_view, main_model)

        self.set_menu_bar_action()
        self.set_image_widget_action()
        self.set_choose_image_area_action()
        self.set_popup_open_project_action()

    def set_popup_open_project_action(self):
        self.main_view.popup_open_project.create_button.clicked.connect(self.popup_open_project_controller.create_project_action)
        self.main_view.popup_open_project.list_project.doubleClicked.connect(
            self.popup_open_project_controller.open_project_action)
        self.main_view.popup_open_project.delete_project.triggered.connect(
            self.popup_open_project_controller.delete_project_action)

    def set_menu_bar_action(self):
        # Images
        self.main_view.menu_bar.load_image_action.triggered.connect(
            lambda: self.menu_bar_controller.load_image_menu_bar(self.popup_open_project_controller.project))

        self.main_view.menu_bar.save_images.triggered.connect(
            lambda: self.menu_bar_controller.save_images()
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

        self.main_view.menu_bar.crop_annotation.triggered.connect(
            self.menu_bar_controller.crop_annotations
        )

        # Project
        self.main_view.menu_bar.save_project.triggered.connect(
            lambda: self.menu_bar_controller.save_project(self.popup_open_project_controller.project)
        )

        self.main_view.menu_bar.close_project.triggered.connect(
            lambda: self.menu_bar_controller.close_project(self.popup_open_project_controller.project)
        )

        # Model
        self.main_view.menu_bar.new_model.triggered.connect(
            lambda: self.menu_bar_controller.create_model()
        )

        self.main_view.menu_bar.load_model.triggered.connect(
            lambda: self.menu_bar_controller.load_model()
        )

        self.main_view.menu_bar.save_model.triggered.connect(
            lambda: self.menu_bar_controller.save_model()
        )

        self.main_view.menu_bar.train.triggered.connect(
            lambda: self.menu_bar_controller.train_model()
        )

        self.main_view.menu_bar.process_from_current.triggered.connect(
            lambda: self.menu_bar_controller.process_image(self.main_view.image_widget.scene.getCurrentAnnotateImage().path)
        )

        self.main_view.menu_bar.process_from_other.triggered.connect(
            lambda: self.menu_bar_controller.process_chosen_image()
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
