

class Account:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def change_id(self, new_id):
        self.id = new_id

    def change_username(self, new_username):
        self.firstname = new_username

    def change_password(self, new_password):
        self.password = new_password


