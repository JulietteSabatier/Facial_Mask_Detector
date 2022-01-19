from PySide6 import QtGui, QtWidgets

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

        # Load Project
        self.close_project = QtGui.QAction("Close (and open new)", self.project)
        self.project.addAction(self.close_project)


        # Model
        self.model = QtWidgets.QMenu("Model", self)

        # Create a model
        self.new_model = QtGui.QAction("New model", self.model)
        self.model.addAction(self.new_model)

        # Load model
        self.load_model = QtGui.QAction("Load model", self.model)
        self.model.addAction(self.load_model)


        #Save model
        self.save_model = QtGui.QAction("Save model", self.model)
        self.save_model.setDisabled(True)
        self.model.addAction(self.save_model)

        # Train the model
        self.train = QtGui.QAction("Train model", self.model)
        self.train.setDisabled(True)
        self.model.addAction(self.train)

        # Process image
        self.process = QtWidgets.QMenu("Process", self.model)
        self.process_from_current = QtGui.QAction("Current image", self.process)
        self.process_from_other = QtGui.QAction("Browse...", self.process)
        self.process.addAction(self.process_from_current)
        self.process.addAction(self.process_from_other)
        self.process.setDisabled(True)
        self.model.addMenu(self.process)


        # Add to menuBar
        self.addMenu(self.image)
        self.addMenu(self.categories)
        self.addMenu(self.annotations)
        self.addMenu(self.project)
        self.addMenu(self.model)

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
        return QtWidgets.QInputDialog.getText(self, "Create a category", "Name of the category", QtWidgets.QLineEdit.Normal)

    def dialog_path_save_categories(self):
        # return QtWidgets.QFileDialog.getExistingDirectory(self, "Save Categories", "Categories")
        return QtWidgets.QFileDialog.getSaveFileName(self, "Save Category in json", "Categories", "Json File (*.json)")

    # Annotations
    def dialog_path_load_annotations(self):
        return QtWidgets.QFileDialog.getOpenFileNames(self, "Load Annotations", "Annotations", "Json File (*.json)")

    def dialog_path_save_annotations(self):
        return QtWidgets.QFileDialog.getSaveFileName(self, "Save Annotations in json", "Annotations", "Json File (*.json)")

    # Project
    def dialog_name_project(self):
        return QtWidgets.QInputDialog.getText(self, "Create a project", "Name of the project", QtWidgets.QLineEdit.Normal)

    def dialog_path_save_project(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Save the Project (Images/ Annotations/Categories)", "Categories")

    def dialog_path_load_project(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Load Project", "Project")

    def dialog_not_a_project(self):
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setText("This directory is not a project")
        message.setDetailedText("A project contains:\n"
                                " - a directory with images \n "
                                "- a file annotations.json \n"
                                " - a file categories.json")
        message.setWindowTitle("Warning Project Directory")
        return message

    def dialog_name_prediction_model(self):
        return QtWidgets.QInputDialog.getText(self, "Create a model", "Name of the model", QtWidgets.QLineEdit.Normal)