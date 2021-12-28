from Model.model_annotator import ModelAnnotator
from View.show_categories_popup import ShowCategoriesPopup
from PySide6 import QtWidgets

class ShowCategoryPopupController:
    main_model: ModelAnnotator
    popup: ShowCategoriesPopup

    def __init__(self, main_model: ModelAnnotator, popup: ShowCategoriesPopup):
        super(ShowCategoryPopupController, self).__init__()
        self.main_model = main_model
        self.popup = popup

    def delete_category(self):
        category = self.popup.delete_category()
        for image in self.main_model.image_list:
            for annotation in image.annotation_list:
                if annotation.title.name == category:
                    message = QtWidgets.QMessageBox()
                    message.setText("You cannot delete an already used category !")
                    message.exec()
                    return False
        self.main_model.delete_category(category)
        self.popup.category_list_widget.takeItem(
            self.popup.category_list_widget.row(self.popup.category_list_widget.currentItem()))

    def rename_category(self):
        res = self.popup.rename_category()
        if res is not None:
            old_name, new_name = res
            self.main_model.rename_category(old_name, new_name)
