from PySide6 import QtGui, QtWidgets, QtCore


class ShowCategoriesPopup(QtWidgets.QDialog):

    def __init__(self):
        super(ShowCategoriesPopup, self).__init__()
        self.resize(600, 300)

        self.category_list_widget = QtWidgets.QListWidget()

        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.category_list_widget)
        self.setLayout(self.box)

        self.category_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.category_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.rename_cat = QtGui.QAction("Rename")
        self.delete_cat = QtGui.QAction("Delete")
        self.category_list_widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.category_list_widget.addAction(self.rename_cat)
        self.category_list_widget.addAction(self.delete_cat)

    def add_categories(self, category_list: list[str]):
        for category in category_list:
            widget_item = QtWidgets.QListWidgetItem(category)
            self.category_list_widget.insertItem(1, widget_item)

    def delete_category(self):
        item_cat = self.category_list_widget.takeItem(
            self.category_list_widget.row(self.category_list_widget.currentItem()))
        name_cat = item_cat.text()
        return name_cat

    def rename_category(self, ):
        new_name, result = QtWidgets.QInputDialog.getText(self, "Rename Categorie", "New name of the category: ")
        if result:
            old_name = self.category_list_widget.currentItem().text()
            self.category_list_widget.currentItem().setText(new_name)
            return old_name, new_name