
class Category:
    name: str

    def __init__(self, category: str):
        """ Create a category which is composed of a name (str)"""
        self.name = category

    def change_name(self, new_name: str):
        """ Modify the name of the category """
        self.name = new_name
