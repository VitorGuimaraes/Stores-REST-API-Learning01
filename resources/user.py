from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", 
    type = str,
    required = True,
    help = "This field cannot be blank.")

_user_parser.add_argument("password", 
    type = str,
    required = True,
    help = "This field cannot be blank.")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        username = data["username"]

        if UserModel.find_by_username(username):
            return {"message": "User '{}' already exists.".format(username)}, 400

        user = UserModel(**data) # "INSERT INTO users VALUES (NULL, ?, ?)"
        user.save_to_db()
        return {"message": "User '{}' created succesfully.".format(username)}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()  
        return {"message": "User '{}' not found".format(user_id)}, 404
        
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"message": "User '{}' deleted.".format(user_id)}, 200

        return {"message": "User '{}' not found".format(user_id)}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity = user.id, fresh = True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        
        return {"message": "Invalid credentials."}, 401