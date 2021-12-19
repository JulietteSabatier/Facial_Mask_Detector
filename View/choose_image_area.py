from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

# Créer le visuel de la scroll bar des nom des images

class MyButton(QtWidgets.QListWidgetItem):
    # Pas encore fini
    def __init__(self, name):
        super(MyButton, self).__init__()
        inside_button = QtWidgets.QPushButton()
        self.setText(name)
        self.setToolTip(name)


class ChooseImageArea(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)

        self.widget = QtWidgets.QWidget()
        self.box = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.box)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedWidth(150)

        self.remove_action = QtGui.QAction("Delete")
        self.rename_action = QtGui.QAction("Rename")
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.remove_action)
        self.addAction(self.rename_action)

    def add_image(self, img_title: str):
        widget_item = QtWidgets.QListWidgetItem(img_title)
        self.insertItem(1, widget_item)

    def delete_image(self):
        item_image = self.takeItem(self.row(self.currentItem()))
        name_image = item_image.text()
        return name_image

    def rename_image_input(self):
        text, result = QtWidgets.QInputDialog.getText(self, "Rename ", "New name of the image: ")
        if result:
            self.currentItem().setText(text)
            return text
