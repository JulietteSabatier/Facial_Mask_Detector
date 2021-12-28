
class Category:
    name: str

    def __init__(self, category: str):
        self.name = category

    def change_name(self, new_name: str):
        self.name = new_name
