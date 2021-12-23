from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from View.custom_scene import CustomScene


class View(QtWidgets.QGraphicsView):  # view of the image
    scene: CustomScene

    def __init__(self, scene):
        QtWidgets.QGraphicsView.__init__(self, scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = scene

    def check_pixel_size(self):
        scene_box = self.scene.getCurrentBox()
        view_box = self.mapFromScene(scene_box)
        print(view_box)
