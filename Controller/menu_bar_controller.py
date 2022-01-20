import os.path

import pre_treatment
from Model.annotate_image import AnnotateImage
from Model.model_annotator import ModelAnnotator
from PySide6 import QtWidgets, QtGui
from View.main_window import MainWindow
from View.show_categories_popup import ShowCategoriesPopup

from Controller.choose_image_area_controller import ChooseImageAreaController
from Controller.image_widget_controller import ImageWidgetController
from Controller.show_category_popup_controller import \
    ShowCategoryPopupController
from mask_recognition import MaskRecognitionModel

# Définition des fonctions qui représentent les action de la menuBar

class MenuBarController:
    main_view: MainWindow
    main_model: ModelAnnotator
    predict_model: MaskRecognitionModel

    choose_image_area_controller: ChooseImageAreaController
    image_widget_controller: ImageWidgetController

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        """ Defines the functions which represent the action of the menubar"""
        self.main_view = main_view
        self.main_model = main_model

        self.choose_image_area_controller = ChooseImageAreaController(main_view, main_model)
        self.image_widget_controller = ImageWidgetController(main_view, main_model)


    # Images
    def load_image_menu_bar(self, project_name: str):
        """ Function which loads one or more images,
        verifies if one image is chosen,
        adds the image to the model and the choose_image_area, and loads the last image in the image_widget """
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
        """ Function which saves only the image in a new directory given by a popup"""
        path = self.main_view.menu_bar.dialog_save_image()
        self.main_model.save_images(path)


    # Categories
    def import_categories(self):
        """ Function which imports and creates the categories from a json or csv file """
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
        """ Function which creates a new category on the model,
        verifies if the name doesn't contain a space or is not '' and fires a popup in this case """
        name, result = self.main_view.menu_bar.dialog_create_new_category()
        if result:
            if (name == "") or (' ' in name) or (" " in name):
                message = QtWidgets.QMessageBox()
                message.setWindowIcon(QtGui.QIcon("iconMask.png"))
                message.setText("Invalid category name")
                message.setWindowTitle("Warning")
                message.exec()

            else:
                res = self.main_model.add_category(name)
                if not res:
                    message = QtWidgets.QMessageBox()
                    message.setWindowIcon(QtGui.QIcon("iconMask.png"))
                    message.setWindowTitle("Warning")
                    message.setText("This category already exist")
                    message.exec()


    def save_categories(self):
        """ Function which saves the categories of the program in a json file
        in the directory given by the user through the popup"""
        path, type_file = self.main_view.menu_bar.dialog_path_save_categories()
        self.main_model.from_categories_to_json(path)


    # Annotations
    def save_annotations(self):
        """ Function which saves the annotation of the program in a json file
        in the directory given by the user through the popup """
        path, type_file = self.main_view.menu_bar.dialog_path_save_annotations()
        self.main_model.from_annotation_to_json(path)


    def load_annotations(self):
        """ Function which loads the annotations present in a json file given by the user through
        the popup """
        path, type_file = self.main_view.menu_bar.dialog_path_load_annotations()
        if len(path) != 0:
            self.main_model.from_json_to_annotation(path[0])


    def crop_annotations(self):
        """Display a popup telling the user the cropped image will be saved in the same directory as the .json they
        will have selected."""
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setWindowTitle("Information")
        message.setWindowIcon(QtGui.QIcon("iconMask.png"))
        message.setText("The images resulting from the crop of the annotations stored in the file you will select will be saved in the same directory as the said file.")
        message.addButton("Cancel", message.RejectRole)
        ok_button = message.addButton("Ok", message.AcceptRole)
        message.exec()
        if message.clickedButton() == ok_button:
            choose_json = QtWidgets.QFileDialog()
            annotations_to_crop = choose_json.getOpenFileName(choose_json, "Select an annotation file", "Annotations", "JSON Files (*.json)")

            if annotations_to_crop is not None:
                pre_treatment.read_json_cut_and_store(annotations_to_crop[0], os.path.dirname(annotations_to_crop[0]))
                message = QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setWindowTitle("Information")
                message.setWindowIcon(QtGui.QIcon("iconMask.png"))
                message.setText("Cropping done.")
                message.exec()


                # Project
    def save_project(self, project_name: str):
        """Saves the current project, copies the images in the right directory, and rewrites annotations.json and
        categories.json """
        if project_name != "":
            path = "Project/" + project_name + "/"
            self.main_model.save_images(path + "Images/")
            self.main_model.from_annotation_to_json(path + "annotations.json")
            self.main_model.from_categories_to_json(path + "categories.json")


    def close_project(self, project_name: str):
        """ Closes the current project, saves it and fires a popup to choose or create another project."""
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


    # Model
    def create_model(self):
        """Creates the prediction model but doesn't train it. Enables the train and process buttons if the name is valid."""
        name, result = self.main_view.menu_bar.dialog_name_prediction_model()

        if result:
            if (name == "") or (' ' in name) or (" " in name):
                message = QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setWindowIcon(QtGui.QIcon("iconMask.png"))
                message.setText("Invalid model name")
                message.setWindowTitle("Warning")
                message.exec()

            else:
                self.predict_model = MaskRecognitionModel(name, "New")
                self.main_view.menu_bar.train.setDisabled(False)
                self.main_view.menu_bar.process.setDisabled(False)
                self.main_view.menu_bar.save_model.setDisabled(False)
                message = QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setWindowIcon(QtGui.QIcon("iconMask.png"))
                message.setText("Model successfully created.")
                message.setWindowTitle("Success")
                message.exec()


    def load_model(self):
        """Loads a model the user will select with a Dialog window. Enables the train and process buttons if the path is valid."""
        dialog_window = QtWidgets.QFileDialog()
        model_path = dialog_window.getOpenFileName(dialog_window,
                                                   "Select Model",
                                                   "Images")
        if model_path is not None:
            self.predict_model = MaskRecognitionModel(model_path[0], "Load")
            self.main_view.menu_bar.train.setDisabled(False)
            self.main_view.menu_bar.process.setDisabled(False)
            self.main_view.menu_bar.save_model.setDisabled(False)
            message = QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setWindowIcon(QtGui.QIcon("iconMask.png"))
            message.setText("Model successfully loaded.")
            message.setWindowTitle("Success")
            message.exec()

    def save_model(self):
        save_dialog_window = QtWidgets.QFileDialog()
        save_path = save_dialog_window.getSaveFileName(save_dialog_window,
                                                       "Save model",
                                                       "Images")
        self.predict_model.save_model(save_path[0])


    def train_model(self):
        path_separator = os.path.sep
        warning_popup = QtWidgets.QMessageBox()
        warning_popup.setIcon(QtWidgets.QMessageBox.Warning)
        warning_popup.setWindowIcon(QtGui.QIcon("iconMask.png"))
        warning_popup.setText("Please make sure the folder you will select contains a 'Train' and a 'Validation' folder.")
        warning_popup.addButton("Cancel", warning_popup.RejectRole)
        ok_button = warning_popup.addButton("Ok", warning_popup.AcceptRole)
        warning_popup.exec()
        if warning_popup.clickedButton() == ok_button:
            select_dir_dialog = QtWidgets.QFileDialog()
            select_dir_dialog.setFileMode(QtWidgets.QFileDialog.Directory)

            selected_dir = select_dir_dialog.getExistingDirectory(select_dir_dialog,
                                                                  "Select a directory",
                                                                  "Images",
                                                                  options = QtWidgets.QFileDialog.ShowDirsOnly)
            train_path = f"{selected_dir}{path_separator}Train"
            validation_path = f"{selected_dir}{path_separator}Validation"

            if os.path.isdir(train_path) and os.path.isdir(validation_path):
                self.predict_model.train_model(train_path, validation_path)
            else:
                warning_popup = QtWidgets.QMessageBox()
                warning_popup.setIcon(QtWidgets.QMessageBox.Critical)
                warning_popup.setWindowIcon(QtGui.QIcon("iconMask.png"))
                warning_popup.setWindowTitle("Error")
                warning_popup.setText("We could not find any folder called 'Train' or 'Validation'.")
                warning_popup.exec()


    def process_image(self, img_path: str):
        mode_input = QtWidgets.QInputDialog()
        mode, did_chose = mode_input.getItem(mode_input, "Mode selection", "Mode", ["categories", "probabilities"], editable=False)
        if did_chose:
            result = self.predict_model.predict(img_path, mode)
            result_msg_box = QtWidgets.QMessageBox()
            result_msg_box.setIcon(QtWidgets.QMessageBox.Information)
            result_msg_box.setWindowIcon(QtGui.QIcon("iconMask.png"))
            result_msg_box.setWindowTitle("Success")
            result_msg_box.setText(result)
            result_msg_box.exec()

    def process_chosen_image(self):
        select_img = QtWidgets.QFileDialog()
        img_path = select_img.getOpenFileName(select_img,
                                              "Open Image",
                                              "Images",
                                              "Image Files (*.png *.jpg *.bpm)")

        if img_path is not None:
            self.process_image(img_path[0])
