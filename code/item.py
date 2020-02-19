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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}


    # Moving code that we re-use out into a class method, this is used by both get & post
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        # 'error first' - we only run the rest of the code if there are no errors.
        #  This helps us move faster, we are not loaidng things we don't need.
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}

        connection = sqlite3.connect('data.db')
        curser = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        curser.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # NB: without the 'WHERE name=?' specifying it would delete the whole table...
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

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
