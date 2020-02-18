# Creating our user class to help us store and access
# data in a better way

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password