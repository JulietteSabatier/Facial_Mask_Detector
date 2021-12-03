import Model.ModelAnnotator as ModelAnnotator
import Model.AnnotateImage as AnnotateImage
from View import MainWindow


class ChooseImageAreaController:
    main_model: ModelAnnotator
    main_view: MainWindow

    def __init__(self, main_model: ModelAnnotator, main_view: MainWindow):
        self.main_view = main_view
        self.main_model = main_model

    def load_image_choose_area(self, image: AnnotateImage):
        self.main_view.get_choose_image_area().add_image(image.get_title())

