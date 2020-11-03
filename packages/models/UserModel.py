from werkzeug.security import generate_password_hash

class UserModel:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get(self):
        return {
            "username": self.username,
            "password": generate_password_hash(self.password)
        }