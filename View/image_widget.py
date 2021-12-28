from Controller.custom_scene_controller import CustomSceneController
from Model.model_annotator import ModelAnnotator
from PySide6 import QtWidgets

from View.custom_scene import CustomScene
from View.view import View


class ImageWidget(QtWidgets.QWidget):  # Central Widget
    main_model : ModelAnnotator
    scene: CustomScene
    view: View
    scene_controller: CustomSceneController
    initialized: bool

    def __init__(self, model: ModelAnnotator, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.initialized = False
        self.main_model = model

    def initialize_scene(self):
        if not self.initialized:
            self.scene = CustomScene(self.main_model, self)
            #self.scene_controller = CustomSceneController(self.scene, self.main_model)
            self.view = View(self.scene)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.view)
            self.adjustSize()
            self.setLayout(layout)
            self.initialized = True
        else:
            self.scene.clear()
            self.scene.currentRect = None
            self.scene.currentBox = None
            self.scene.annot_list = []
            self.scene.currentAnnot = None
            self.scene.rect_list = []
            self.scene.box_list = []

