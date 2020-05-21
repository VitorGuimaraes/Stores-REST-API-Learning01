from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager 
from datetime import timedelta

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# If the flask extensions raises an error, it can send their own error messages
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
api = Api(app)
# Token Expiration Time
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)

jwt = JWTManager(app) 

@jwt.user_claims_loader
def add_claims_to_jwt(identity): # Instead of hard-coding, you should read from a config file or a database
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

api.add_resource(Item, "/item/<string:name>") 
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)