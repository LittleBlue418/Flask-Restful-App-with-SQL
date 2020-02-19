# Importing our safe string method and the user class that
# we created in user.py we can import directly as the files
# are in the same folder
from werkzeug.security import safe_str_cmp
from user import User


# Using out user class to create user objects
users = [
    User(1, 'bob', 'asdf')
]


# These functions help us quickly access users by either
# username or by id, preventing us from having to itterate
# over the list each time we want to access a user
username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


# Identifying the user by comparing the username and
# password they enter to the username mapping
# Returing the user, fed to JWT to make the token
def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


# Used when requesting an end point where authentication needed
# Payload comes from request, contains user id, search on the
# id mapping with this. If match then we know user is authenticated
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
