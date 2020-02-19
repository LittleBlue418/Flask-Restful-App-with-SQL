import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Auto incrementing id, now we only have to specify the username and
# the password, the INTEGER PRIMARY KEY does the heavy lifting
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()

connection.close()