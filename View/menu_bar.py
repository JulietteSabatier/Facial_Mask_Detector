from PySide6 import QtWidgets
from PySide6 import QtGui


# Créer la menu bar

class MenuBar(QtWidgets.QMenuBar):

    def __init__(self):
        super().__init__()
        # Images
        self.image = QtWidgets.QMenu("Image", self)

        # Load image
        self.load_image_action = QtGui.QAction("Load Image", self)
        self.image.addAction(self.load_image_action)

        # Delete Image
        self.delete_image = QtGui.QAction("Delete Image", self.image)
        self.image.addAction(self.delete_image)

        #  Categories
        self.categories = QtWidgets.QMenu("Categories", self)

        # Import from csv
        self.import_csv = QtGui.QAction("Import from cvs", self.categories)
        self.categories.addAction(self.import_csv)

        # Import from json
        self.import_json = QtGui.QAction("Import from json", self.categories)
        self.categories.addAction(self.import_json)

        # Rename categories
        self.rename = QtGui.QAction("Rename", self.categories)
        self.categories.addAction(self.rename)

        # Show all
        self.show_all = QtGui.QAction("Show All", self.categories)
        self.categories.addAction(self.show_all)

        # Create new
        self.create_new = QtGui.QAction("Create New", self.categories)
        self.categories.addAction(self.create_new)

        # Save
        self.save = QtWidgets.QMenu("Save", self)

        # Save Categories
        self.save_categories = QtGui.QAction("Categories", self.save)
        self.save.addAction(self.save_categories)

        # Save Annotations
        self.save_annotation = QtGui.QAction("Annotation", self.save)
        self.save.addAction(self.save_annotation)

        # Save Image
        self.save_images = QtGui.QAction("Images", self.save)
        self.save.addAction(self.save_images)

        # Add to menuBar
        self.addMenu(self.image)
        self.addMenu(self.categories)
        self.addMenu(self.save)

    def widget_load_image(self):
        image = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image",
                                                       "Images",
                                                       "Image Files (*.png *.jpg *.bpm)")
        return image
