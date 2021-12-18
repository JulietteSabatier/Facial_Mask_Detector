from Model.model_annotator import ModelAnnotator

from View.show_categories_popup import ShowCategoriesPopup

class ShowCategoryPopupController:
    main_model: ModelAnnotator
    popup: ShowCategoriesPopup

    def __init__(self, main_model: ModelAnnotator, popup: ShowCategoriesPopup):
        super(ShowCategoryPopupController, self).__init__()
        self.main_model = main_model
        self.popup = popup

    def delete_category(self):
        category = self.popup.delete_category()
        self.main_model.delete_category(category)

    def rename_category(self):
        old_name, new_name = self.popup.rename_category()
        self.main_model.rename_category(old_name, new_name)
