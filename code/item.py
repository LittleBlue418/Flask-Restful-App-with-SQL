import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


# Our items class, with the different end points as methods. Note
# that it inherrits from the Resource class.
class Item(Resource):
    # The parse functionality belongs to the class as it is shared
    # by more than one method
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # This method has the JavaScript Web Token required decorator, the user
    # must be authenticated and have an auth key to do anything with it.
    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}


    def post(self, name):
        # Using a lambda function to filter, here we are working 'error first'
        # which will mean we only run the rest of the code if there are no
        # errors. This helps us move faster, we are not loaidng things we don't need.
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201


    def delete(self, name):
        global items
        # We need the list method here as we are making a new list from all
        # items that do NOT match
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}


    def put(self, name):
        request_data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item


# A seporate class with a seporate end point to get all of the items.
class ItemList(Resource):
    def get(self):
        return {'items': items}
