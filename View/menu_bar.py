from PySide6 import QtWidgets
from PySide6 import QtGui


# Créer la menu bar

class MenuBar(QtWidgets.QMenuBar):

    def __init__(self):
        super().__init__()
        # Images
        self.image = QtWidgets.QMenu("Image", self)

        # Load image
        self.load_image_action = QtGui.QAction("Load", self)
        self.image.addAction(self.load_image_action)

        # Save Image
        self.save_images = QtGui.QAction("Save", self.image)
        self.image.addAction(self.save_images)

        #  Categories
        self.categories = QtWidgets.QMenu("Categories", self)

        # Import
        self.import_cat = QtGui.QAction("Import", self.categories)
        self.categories.addAction(self.import_cat)

        # Show all
        self.show_all = QtGui.QAction("Show All", self.categories)
        self.categories.addAction(self.show_all)

        # Create new
        self.create_new = QtGui.QAction("Create New", self.categories)
        self.categories.addAction(self.create_new)

        # Save categories
        self.save_categories = QtGui.QAction("Save", self.categories)
        self.categories.addAction(self.save_categories)

        # Annotations
        self.annotations = QtWidgets.QMenu("Annotations", self)

        # Save Annotations
        self.save_annotation = QtGui.QAction("Save", self.annotations)
        self.annotations.addAction(self.save_annotation)

        # Load Annotations
        self.load_annotation = QtGui.QAction("Load", self.annotations)
        self.annotations.addAction(self.load_annotation)

        # Project
        self.project = QtWidgets.QMenu("Project", self)

        # Save Project
        self.save_project = QtGui.QAction("Save", self.project)
        self.project.addAction(self.save_project)

        # Save Project
        self.load_project = QtGui.QAction("Load", self.project)
        self.project.addAction(self.load_project)

        # Add to menuBar
        self.addMenu(self.image)
        self.addMenu(self.categories)
        self.addMenu(self.annotations)
        self.addMenu(self.project)

    # Images
    def widget_load_image(self):
        return QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image",
                                                       "Images",
                                                       "Image Files (*.png *.jpg *.bpm)")

    def dialog_save_image(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Save the images", "Images")

    # Categories
    def widget_import_categories(self):
        return QtWidgets.QFileDialog.getOpenFileNames(self, "Open categories", "Categories", "Data files (*.csv *.json)")

    def dialog_create_new_category(self):
        return QtWidgets.QInputDialog.getText(self, "Create a category", "Name of the category")

    def dialog_path_save_categories(self):
        return QtWidgets.QFileDialog.getSaveFileName(self, "Save Category in json", "Categories", "Json File (*.json)")

    # Annotations
    def dialog_path_load_annotations(self):
        return QtWidgets.QFileDialog.getOpenFileNames(self, "Load Annotations", "Annotations", "Json File (*.json)")

    def dialog_path_save_annotations(self):
        return QtWidgets.QFileDialog.getSaveFileName(self, "Save Annotations in json", "Annotations", "Json File (*.json)")

    # Project
    def dialog_path_save_project(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Save the Project (Images/ Annotations/Categories)", "Categories")

    def dialog_path_load_project(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Load Project", "Project")