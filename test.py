import sqlite3

# Connecting to our 'database' which is a file in the folder
connection = sqlite3.connect('data.db')

# Initiating our cursor
cursor = connection.cursor()

# Creating the table we will store data in
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# Populating the table with our first user
user = (1, 'Jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# Inserting many users
users = [
    (2, 'Josie', 'asdf'),
    (3, 'Jannice', 'a455'),
    (4, 'Joyce', 'gh7da'),
    (5, 'Julia', 'fhsls912')
]
cursor.executemany(insert_query, users)

# Retrieving data
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# Saving our changes to the database / file
connection.commit()

# Closing our connection after use
connection.close()