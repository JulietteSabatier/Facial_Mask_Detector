from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from shapely.geometry import Point, box

from Model.selection_box import Box


class View(QtWidgets.QGraphicsView):  # view of the image

    def __init__(self, scene):
        QtWidgets.QGraphicsView.__init__(self, scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = scene
        self.scene.set_view(self)

    def check_pixel_size(self, scene_box: Box):
        """Checks if the given box is big enough to be valid. That means the box has to be at least 5 pixels wide/high
        and its area must be at least 40 pixels."""

        view_box = self.mapFromScene(scene_box.getTopLeft().getX(), scene_box.getTopLeft().getY(), scene_box.getWidth(), scene_box.getHeight())
        top_left, top_right, bottom_left, bottom_right = view_box
        top_left_point = Point(top_left.x(), top_left.y())
        top_right_point = Point(top_right.x(), top_right.y())
        bottom_left_point = Point(bottom_left.x(), bottom_left.y())
        bottom_right_point = Point(bottom_right.x(), bottom_right.y())
        return top_left_point.distance(top_right_point) < 5 \
               or top_left_point.distance(bottom_left_point) < 5 \
               or bottom_right_point.distance(top_right_point) < 5 \
               or bottom_right_point.distance(bottom_left_point) < 5 \
               or top_left_point.distance(top_right_point) * top_left_point.distance(bottom_left_point) < 40
               #or box(top_left.x(), top_left.y(), bottom_right.x(), bottom_right.y()).area < 40 ne marche pas mais je
               #le laisse si jamais je trouve pourquoi (un jour peut-être)
