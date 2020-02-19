# Importing gives out class the ability to interact with sqlite
import sqlite3


# Creating our user class to help us store and access
# data in a better way
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # select every row, a row per user, ? is a where clause
        # only those rows where the username matches the parametor
        query = "SELECT * FROM users WHERE username=?"
        # parametors must always be in the form of a tuple (even if just 1)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None


        connection.close()
        return user