# Représente les position

class Position:
    left_up_point: (int, int)
    right_down_point: (int, int)

    def __init__(self, left_up: (int, int), right_down: (int, int)):
        self.right_down_point = right_down
        self.left_up_point = left_up

    def get_left_up_point(self):
        return self.left_up_point

    def get_right_down_point(self):
        return self.right_down_point

    def set_left_up_point(self, point: (int, int)):
        self.left_up_point = point

    def set_right_down_point(self, point: (int, int)):
        self.right_down_point = point

    def from_position_to_json(self):
        return {"left_up": {
                    "abs": self.left_up_point[0],
                    "ord": self.left_up_point[1]},

                "right_down": {
                    "abs": self.right_down_point[0],
                    "ord": self.right_down_point[1]}
                }
