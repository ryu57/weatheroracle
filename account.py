

class Account:
    def __init__(self, id):
        self.id = id
        self.location = "Toronto"


    def change_id(self, new_id):
        self.id = new_id

    def change_location(self, location):
        self.location = location

