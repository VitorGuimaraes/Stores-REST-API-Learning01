from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel


class Item(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type = float,
                        required = True,
                        help = "this field can't be left blank!"
                        )
    parser.add_argument("store_id",
                        type = int,
                        required = True,
                        help = "Every item needs a store_id."
                        )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item '{}' not found.".format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) # data["price"], data["store_id"]
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500 # Internal Server Error

        return item.json(), 201 # 201 created

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item '{}' deleted.".format(name)}
        return {"message": "Item '{}' not found.".format(name)}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data) # data["price"], data["store_id"]
                    
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]} 
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))} # the same 

        # Use map, filter, reduce if your team is using others languages too. 
        # Else use list comprehension 
        # List comprehension is a bit faster! 