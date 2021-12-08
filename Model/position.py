# Représente les position

class Position:
    left_up_point: (int, int)
    left_down_point: (int, int)
    right_up_point: (int, int)
    right_down_point: (int, int)

    def __init__(self, left_up: (int, int), left_down: (int, int), right_up: (int, int), right_down: (int, int)):
        self.right_up_point = right_up
        self.right_down_point = right_down
        self.left_up_point = left_up
        self.left_down_point = left_down

    def get_left_up_point(self):
        return self.left_up_point

    def get_left_down_point(self):
        return self.left_down_point

    def get_right_up_point(self):
        return self.right_up_point

    def get_right_down_point(self):
        return self.right_down_point

    def set_left_up_point(self, point: (int, int)):
        self.left_up_point = point

    def set_left_down_point(self, point: (int, int)):
        self.left_down_point = point

    def set_right_up_point(self, point: (int, int)):
        self.right_up_point = point

    def set_right_down_point(self, point: (int, int)):
        self.right_down_point = point

