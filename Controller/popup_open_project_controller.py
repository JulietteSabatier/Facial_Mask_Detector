import json
import shutil
from pathlib import Path

from View.main_window import MainWindow
from Model.model_annotator import ModelAnnotator
import os
from PySide6 import QtGui, QtWidgets, QtCore


class PopupOpenProjectController:
    main_view: MainWindow
    main_model: ModelAnnotator
    project: str

    def __init__(self, main_view: MainWindow, main_model: ModelAnnotator):
        self.main_view = main_view
        self.main_model = main_model
        self.project = ""

    def create_project_action(self):
        name = self.dialog_name_project()
        if name is not None:
            path = "Project/" + name
            if not os.path.exists(path + "/Images"):
                path_to_create = Path(path+'/Images')
                path_to_create.mkdir(parents=True, exist_ok=True)
            data = {}
            annot_json = open(path + "/annotations.json", 'w')
            cat_json = open(path + "/categories.json", 'w')
            json.dump(data, annot_json)
            json.dump(data, cat_json)
            self.project = name

    def delete_project_action(self):
        path = "Project/" + self.main_view.popup_open_project.list_project.currentItem().text()
        try:
            self.main_view.popup_open_project.list_project.takeItem(
                self.main_view.popup_open_project.list_project.row(
                    self.main_view.popup_open_project.list_project.currentItem()))
            shutil.rmtree(path)
        except:
            self.main_view.popup_open_project.dialog_no_project()
            self.main_view.popup_open_project.list_project.removeItemWidget(
                self.main_view.popup_open_project.list_project.currentItem())

    def open_project_action(self):
        path = "Project/" + self.main_view.popup_open_project.list_project.currentItem().text()
        if (os.path.exists(path + "/Images")
                and os.path.exists(path + "/annotations.json")
                and os.path.exists(path + "/categories.json")):
            self.main_model.from_json_to_categories(path + "/categories.json")
            self.main_model.from_json_to_annotation(path + "/annotations.json")
            self.project = path.split("/")[-1]
            self.main_view.choose_image_area.load_all_images()
            self.main_view.popup_open_project.force_close = False
            self.main_view.popup_open_project.close()
        else:
            self.main_view.popup_open_project.dialog_no_project()
            self.main_view.popup_open_project.list_project.removeItemWidget(
                self.main_view.popup_open_project.list_project.currentItem())

    def dialog_name_project(self):
        project_name, result = QtWidgets.QInputDialog.getText(
            self.main_view.popup_open_project, "Create a project", "Name of the project")
        if not result:
            return None
        while os.path.exists("Project/" + project_name):
            project_name, result = QtWidgets.QInputDialog.getText(
                self.main_view.popup_open_project, "Create a project",
                "The previous name already exist, write a new one")
            if not result:
                project_name = None
                break
        if project_name is not None:
            self.main_view.popup_open_project.force_close = False
            self.main_view.popup_open_project.close()
        return project_name
