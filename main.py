import sys
import getpass
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Slot

import ChooseImageArea
import ImageWidget


class ImageAnnotator(QtWidgets.QMainWindow):  # main window
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.w = ImageWidget.ImageWidget()
        self.c = ChooseImageArea.ChooseImageArea()

        page_layout = QtWidgets.QHBoxLayout()
        page_layout.addWidget(self.c)
        page_layout.addWidget(self.w)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(page_layout)
        self.setCentralWidget(central_widget)

        self.init_ui()

        # Scroll area

    def init_ui(self):
        self.baseSize()
        self.windowTitle()
        self.setWindowTitle("Image Annotator")
        icon = QtGui.QIcon("iconMask.png")
        self.setWindowIcon(icon)
        self.resize(800, 600)
        self.create_menu_bar()
        self.show()

    def create_menu_bar(self):
        menu_bar = QtWidgets.QMenuBar(self)

        # Images
        image = QtWidgets.QMenu("Image", menu_bar)

        # Load image
        load_image = QtGui.QAction("Load Image", image)
        image.addAction(load_image)
        # Load image on the ScrollArea and on the ImageWidget
        load_image.triggered.connect(self.load_image)

        # Delete Image
        delete_image = QtGui.QAction("Delete Image", image)
        image.addAction(delete_image)
        # delete_image.triggered.connect(slot_to_delete_an_image)

        #  Categories
        categories = QtWidgets.QMenu("Categories", menu_bar)

        # Import from csv
        import_csv = QtGui.QAction("Import from cvs", categories)
        categories.addAction(import_csv)
        # import_csv.triggered.connect(slot_to_import_categories_from_cvs)

        # Import from json
        import_json = QtGui.QAction("Import from json", categories)
        categories.addAction(import_json)
        # import_json.triggered.connect(slot_to_import_categories_from_json)

        # Rename categories
        rename = QtGui.QAction("Rename", categories)
        categories.addAction(rename)
        # rename.triggered.connect(slot_to_rename_categories)

        # Show all
        show_all = QtGui.QAction("Show All", categories)
        categories.addAction(show_all)
        # show_all.triggerred.connect(slot_to_show_all)

        # Create new
        create_new = QtGui.QAction("Create New", categories)
        categories.addAction(create_new)
        # create_new.triggered.connect(slot_to_create_new_categorie)

        # Save
        save = QtWidgets.QMenu("Save", menu_bar)

        # Save Categories
        save_categories = QtGui.QAction("Categories", save)
        save.addAction(save_categories)
        # save_categories.triggered.connect(slot_to_save_categories)

        # Save Annotations
        save_annotation = QtGui.QAction("Annotation", save)
        save.addAction(save_annotation)
        # save_annotation.triggered.connect(slot_to_save_annotation)

        # Save Image
        save_images = QtGui.QAction("Images", save)
        save.addAction(save_images)
        # save_images.triggered.connect(slot_to_save_images

        # Add to menuBar
        menu_bar.addMenu(image)
        menu_bar.addMenu(categories)
        menu_bar.addMenu(save)

        # Define menuBar
        self.setMenuBar(menu_bar)

    @Slot()
    def load_image(self):
        basePath = "/users/" + getpass.getuser() + "/pictures"
        img = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                     "Open Image",
                                                     basePath,
                                                     "Image Files (*.png *.jpg *.bpm)")[0]
        if len(img) != 0:
            self.c.add_image(img)
            self.w.load_image(img)

if __name__ == '__main__':  # main
    app = QtWidgets.QApplication(sys.argv)
    imageAnnotator = ImageAnnotator()
    imageAnnotator.resize(640, 480)
    imageAnnotator.show()
    sys.exit(app.exec())
