from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name) 
        if store:
            return store.json() 
        return {"message": "Store '{}' not found.".format(name)}, 404 

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error ocurred while creating the store."}, 500
        return store.json(), 201 # 201 created

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store: 
            store.delete_from_db()
            return {"message": "Store '{}' deleted".format(name)}
        return {"message": "Store '{}' not found.".format(name)}
        
class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}

        # return {"items": list(map(lambda x: x.json(), ItemModel.find_all()))} # the same 

        # Use map, filter, reduce if your team is using others languages too. 
        # Else use list comprehension 
        # List comprehension is a bit faster! 