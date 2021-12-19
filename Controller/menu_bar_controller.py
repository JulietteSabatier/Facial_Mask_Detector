import os.path

from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from Model.annotation import Annotation
from Model.position import Position
from Controller.choose_image_area_controller import ChooseImageAreaController
from Controller.image_widget_controller import ImageWidgetController
from Controller.show_category_popup_controller import ShowCategoryPopupController

from View.main_window import MainWindow
from View.show_categories_popup import ShowCategoriesPopup


# Définition des fonctions qui représentent les action de la menuBar


class MenuBarController:
    main_view: MainWindow
    main_model: ModelAnnotator

    choose_image_area_controller: ChooseImageAreaController
    image_widget_controller: ImageWidgetController

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        self.main_view = main_view
        self.main_model = main_model

        self.choose_image_area_controller = ChooseImageAreaController(main_view, main_model)
        self.image_widget_controller = ImageWidgetController(main_view, main_model)

    # Images
    def load_image_menu_bar(self):

        # Charge un ou plusieurs images la dernière seulement s'affiche dans la graphicView
        # Ne charge pas les annotations
        imgs = self.main_view.menu_bar.widget_load_image()

        if len(imgs[0]) != 0:

            for i in range(len(imgs[0])):
                path = imgs[0][i]
                title = path.split("/")[-1].split(".")[0]
                image = AnnotateImage(path, title, [])

                # Ajouter l'image dans la base
                self.main_model.add_image(image)
                # Envoyer les infos a la scroll area
                self.choose_image_area_controller.create_button(image)
                # Envoyer les infos a au widget image
                self.image_widget_controller.load_image_widget(image)

    def save_images(self):
        path = self.main_view.menu_bar.dialog_save_image()
        self.main_model.save_images(path)
        print("Save Images")

    # Categories
    def import_categories(self):
        categories = self.main_view.menu_bar.widget_import_categories()
        if len(categories[0]) != 0:
            import_type = categories[0][0].split("/")[-1].split(".")[-1]
            if import_type == "json":
                self.main_model.from_json_to_categories(categories[0][0])
            elif import_type == "csv":
                self.main_model.from_csv_to_categories(categories[0][0])

    def show_categories(self):
        popup = ShowCategoriesPopup()
        popup_controller = ShowCategoryPopupController(self.main_model, popup)
        popup.add_categories(self.main_model.category_list)

        popup.delete_cat.triggered.connect(popup_controller.delete_category)
        popup.rename_cat.triggered.connect(popup_controller.rename_category)

        popup.exec()

    def create_new_category(self):
        name, result = self.main_view.menu_bar.dialog_create_new_category()
        self.main_model.add_category(name)

    def save_categories(self):
        path, type_file = self.main_view.menu_bar.dialog_path_save_categories()
        self.main_model.from_categories_to_json(path)

    # Annotations
    def save_annotations(self):
        path, type_file = self.main_view.menu_bar.dialog_path_save_annotations()
        self.main_model.from_annotation_to_json(path)

    def load_annotations(self):
        path, type_file = self.main_view.menu_bar.dialog_path_load_annotations()
        self.main_model.from_json_to_annotation(path[0])

    # Project
    def create_project(self):
        name, result = self.main_view.menu_bar.dialog_name_project()
        if result:
            path = "Project/"+name
            if not os.path.exists(path+"/Images"):
                os.makedirs(path+"/Images")
            open(path+"/annotations.json", 'w')
            open(path+"/categories.json", 'w')

    def save_project(self):
        path = self.main_view.menu_bar.dialog_path_load_project()
        print("Save project")

    def load_project(self):
        path = self.main_view.menu_bar.dialog_path_save_project()
        if (os.path.exists(path+"/Images")
            and os.path.exists(path+"/annotations.json")
            and os.path.exists(path+"/categories.json")):
            self.main_model.from_json_to_annotation(path+"/annotations.json")
            self.main_model.from_json_to_categories(path+"/categories.json")
        else:
            self.main_view.menu_bar.dialog_not_a_project()