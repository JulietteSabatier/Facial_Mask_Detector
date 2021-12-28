from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from PySide6 import QtWidgets
from View.main_window import MainWindow
from View.show_categories_popup import ShowCategoriesPopup

from Controller.choose_image_area_controller import ChooseImageAreaController
from Controller.image_widget_controller import ImageWidgetController
from Controller.show_category_popup_controller import \
    ShowCategoryPopupController

# Définition des fonctions qui représentent les action de la menuBar

class MenuBarController:
    main_view: MainWindow
    main_model: ModelAnnotator

    choose_image_area_controller: ChooseImageAreaController
    image_widget_controller: ImageWidgetController

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        """ Define the functions which represent the action of the menubar """
        self.main_view = main_view
        self.main_model = main_model

        self.choose_image_area_controller = ChooseImageAreaController(main_view, main_model)
        self.image_widget_controller = ImageWidgetController(main_view, main_model)

    # Images
    def load_image_menu_bar(self, project_name: str):
        """ Function which load one or more images
        verify if one image is chosen,
        add the image in the model, the choose_image_area and load the last in the image_widget """
        imgs = self.main_view.menu_bar.widget_load_image()

        if len(imgs[0]) != 0:

            for i in range(len(imgs[0])):
                path = imgs[0][i]
                title = path.split("/")[-1].split(".")[0]
                #                new_path = "Project/"+project_name+"/"+title
                image = AnnotateImage(path, title, [])

                # Ajouter l'image dans la base
                self.main_model.add_image(image)
                # Envoyer les infos a la scroll area
                self.choose_image_area_controller.create_button(image)
                # Envoyer les infos a au widget image
                self.image_widget_controller.load_image_widget(image)

    def save_images(self):
        """ Function which save only the image on a new directory given by a popup"""
        path = self.main_view.menu_bar.dialog_save_image()
        self.main_model.save_images(path)

    # Categories
    def import_categories(self):
        """ Function which import and create the categories given from a json or csv file """
        categories = self.main_view.menu_bar.widget_import_categories()
        if len(categories[0]) != 0:
            import_type = categories[0][0].split("/")[-1].split(".")[-1]
            if import_type == "json":
                self.main_model.from_json_to_categories(categories[0][0])
            elif import_type == "csv":
                self.main_model.from_csv_to_categories(categories[0][0])

    def show_categories(self):
        """ Function which """
        popup = ShowCategoriesPopup()
        popup_controller = ShowCategoryPopupController(self.main_model, popup)
        popup.add_categories(self.main_model.category_list)

        popup.delete_cat.triggered.connect(popup_controller.delete_category)
        popup.rename_cat.triggered.connect(popup_controller.rename_category)

        popup.exec()

    def create_new_category(self):
        """ Function which create a new category on the model
        verify if the name doesn't contains a space or is not '' and fire a popup int this case """
        name, result = self.main_view.menu_bar.dialog_create_new_category()
        if result:
            if (name == "") or (' ' in name):
                message = QtWidgets.QMessageBox()
                message.setText("Invalid category name")
                message.setWindowTitle("Warning")
                message.exec()

            else:
                res = self.main_model.add_category(name)
                if not res:
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Warning")
                    message.setText("This category already exist")
                    message.exec()

    def save_categories(self):
        """ Function which save the categories of the program in a json file
        on the directory given by the user on the popup"""
        path, type_file = self.main_view.menu_bar.dialog_path_save_categories()
        self.main_model.from_categories_to_json(path)

    # Annotations
    def save_annotations(self):
        """ Function which save the annotation of the program in a json file
        one the directory given by the user on the popup """
        path, type_file = self.main_view.menu_bar.dialog_path_save_annotations()
        self.main_model.from_annotation_to_json(path)

    def load_annotations(self):
        """ Function which load the annotations present in a json file given by the user thanks to
        the popup """
        path, type_file = self.main_view.menu_bar.dialog_path_load_annotations()
        if len(path) != 0:
            self.main_model.from_json_to_annotation(path[0])

    # Project
    def save_project(self, project_name: str):
        """ Save the current project copy the images in the good directory and rewrite annotations.json and
        categories.json """
        if project_name != "":
            path = "Project/" + project_name + "/"
            self.main_model.save_images(path + "Images/")
            self.main_model.from_annotation_to_json(path + "annotations.json")
            self.main_model.from_categories_to_json(path + "categories.json")

    def close_project(self, project_name: str):
        """ Close the current project and save it, fire the popup to choose another project or create a new one"""
        self.save_project(project_name)
        self.main_model.category_list = []
        self.main_model.image_list = []
        self.main_view.choose_image_area.clear()
        try:
            self.main_view.image_widget.scene.clear()
        except:
            pass
        self.main_view.popup_open_project.force_close = True
        self.main_view.popup_open_project.update_list_project()
        self.main_view.popup_open_project.show()
