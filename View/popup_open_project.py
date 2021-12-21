import os.path
import sys

from PySide6 import QtGui, QtWidgets, QtCore


class PopupOpenProject(QtWidgets.QDialog):

    def __init__(self):
        super(PopupOpenProject, self).__init__()

        self.resize(600, 300)
        self.setWindowTitle("Image Annotator Project")
        self.force_close = True

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.create_button = QtWidgets.QPushButton("Create Project")
        self.text_load = QtWidgets.QLabel("Load a project below")
        self.list_project = QtWidgets.QListWidget()

        self.list_project.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.delete_project = QtGui.QAction("Delete")
        self.list_project.addAction(self.delete_project)

        # Layout
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.create_button)
        self.box.addWidget(self.text_load)
        self.box.addWidget(self.list_project)
        self.setLayout(self.box)
        self.list_project.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_project.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Liste des projets
        list_project = os.listdir("Project")
        list_path_project = [os.path.join("Project", x) for x in list_project]

        for i in range(len(list_project)):
            if (os.path.exists(list_path_project[i] + "/Images")
                    and os.path.exists(list_path_project[i] + "/annotations.json")
                    and os.path.exists(list_path_project[i] + "/categories.json")):
                item = QtWidgets.QListWidgetItem(list_project[i].title())
                self.list_project.addItem(item)

    def closeEvent(self, event) -> None:
        if self.force_close:
            sys.exit()

    def dialog_no_project(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setText("This project doesn't exist")

    def update_list_project(self) -> None:
        list_projects = os.listdir("Project")
        list_path_project = [os.path.join("Project", x) for x in list_projects]

        for i in range(len(list_projects)):
            find = False
            for j in range(self.list_project.count()):
                if list_projects[i].title().upper() == self.list_project.item(j).text().upper():
                    find = True
            if not find:
                item = QtWidgets.QListWidgetItem(list_projects[i].title())
                self.list_project.addItem(item)
            else:
                continue
