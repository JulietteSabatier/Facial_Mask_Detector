from PySide6 import QtWidgets
from PySide6 import QtGui


# Créer la menu bar

class MenuBar(QtWidgets.QMenuBar):
    image: QtWidgets.QMenu
    categories: QtWidgets.QMenu
    save: QtWidgets.QMenu

    def __init__(self):
        super().__init__()
        # Images
        self.image = QtWidgets.QMenu("Image", self)

        # Load image
        self.load_image_action = QtGui.QAction("Load Image", self)
        self.image.addAction(self.load_image_action)

        # Delete Image
        delete_image = QtGui.QAction("Delete Image", self.image)
        self.image.addAction(delete_image)

        #  Categories
        self.categories = QtWidgets.QMenu("Categories", self)

        # Import from csv
        import_csv = QtGui.QAction("Import from cvs", self.categories)
        self.categories.addAction(import_csv)

        # Import from json
        import_json = QtGui.QAction("Import from json", self.categories)
        self.categories.addAction(import_json)

        # Rename categories
        rename = QtGui.QAction("Rename", self.categories)
        self.categories.addAction(rename)

        # Show all
        show_all = QtGui.QAction("Show All", self.categories)
        self.categories.addAction(show_all)

        # Create new
        create_new = QtGui.QAction("Create New", self.categories)
        self.categories.addAction(create_new)

        # Save
        self.save = QtWidgets.QMenu("Save", self)

        # Save Categories
        save_categories = QtGui.QAction("Categories", self.save)
        self.save.addAction(save_categories)

        # Save Annotations
        save_annotation = QtGui.QAction("Annotation", self.save)
        self.save.addAction(save_annotation)

        # Save Image
        save_images = QtGui.QAction("Images", self.save)
        self.save.addAction(save_images)

        # Add to menuBar
        self.addMenu(self.image)
        self.addMenu(self.categories)
        self.addMenu(self.save)

    def widget_load_image(self):
        image = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image",
                                                       "Images",
                                                       "Image Files (*.png *.jpg *.bpm)")
        return image
