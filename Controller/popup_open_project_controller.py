import json

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
                os.makedirs(path + "/Images")
            data = {}
            annot_json = open(path + "/annotations.json", 'w')
            cat_json = open(path + "/categories.json", 'w')
            json.dump(data, annot_json)
            json.dump(data, cat_json)
            self.project = name

    def delete_project_action(self):
        path = "Project/" + self.main_view.popup_open_project.list_project.currentItem().text()
        try:
            os.remove(path)
        except:
            self.dialog_no_project()
            self.main_view.popup_open_project.list_project.removeItemWidget(
                self.main_view.popup_open_project.list_project.currentItem())

    def open_project_action(self):
        path = "Project/" + self.main_view.popup_open_project.list_project.currentItem().text()
        if (os.path.exists(path + "/Images")
                and os.path.exists(path + "/annotations.json")
                and os.path.exists(path + "/categories.json")):
            self.main_model.from_json_to_annotation(path + "/annotations.json")
            self.main_model.from_json_to_categories(path + "/categories.json")
            self.project = path.split("/")[-1]
            self.main_view.popup_open_project.close()
        else:
            self.dialog_no_project()
            self.main_view.popup_open_project.list_project.removeItemWidget(
                self.main_view.popup_open_project.list_project.currentItem())

    def dialog_name_project(self):
        project_name, result = QtWidgets.QInputDialog.getText(
            self.main_view.popup_open_project, "Create a project", "Name of the project")
        while os.path.exists("Project/" + project_name):
            project_name, result = QtWidgets.QInputDialog.getText(
                self.main_view.popup_open_project, "Create a project", "The previous name already exist, write a new one")
            if not result:
                project_name = None
                break
        if project_name is not None:
            self.main_view.popup_open_project.reject()
        return project_name

    def dialog_no_project(self):
        QtWidgets.QMessageBox.setText("This project doesn't exist")
