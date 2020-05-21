from flask import Flask
from flask_restful import Api
from flask_jwt import JWT 
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# If the flask extensions raises an error, it can send their own error messages
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "vitor" # it should be secret
api = Api(app)
# Change the url to the authentication endpoint
# app.config['JWT_AUTH_URL_RULE'] = "/login"
# Token Expiration Time
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)

jwt = JWT(app, authenticate, identity) # /auth endpoint
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)