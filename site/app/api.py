""" module used to create api routes and action with routes """
from functools import wraps
from flask import Blueprint, jsonify, request
import jwt

from .validators.validators import Validator
from .controllers import todo_controller as tc
from .controllers import user_controller as uc

# create blueprint
api = Blueprint('api', __name__)
# create validator
validator = Validator()
SECRET = "Secret"

# variable to save default response messages
errors = {
    "0": "Token is missing in header",
    "1": "User does not exist",
    "2": "Invalid token",
    "3": "Success",
    "4": "To-do updated successfully",
    "5": "To-do does not exist",
    "6": "To-do removed successfully",
    "7": "To-do added successfully",
    "8": "User registered successfully"
}

def response_maker(message_id, status, opt_key=None, opt_value=None):
    """ method used to create response message """
    if opt_key:
        return jsonify({ "Message": errors[str(message_id)], str(opt_key):str(opt_value) }, status)
    return jsonify({ "Message": errors[str(message_id)] }, status)

def token_validation(func):
    """ method to wrap/decorate routes """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if not "auth-token" in request.headers:
            return response_maker(0, 406)

        token = request.headers["auth-token"]

        try:
            # token - token from client
            # secret_key - secret key for algorithm
            # algorithms - decoding algorithm - must match the algorithm used to encode.
            # Decode algorithms is a list of algorithms. Algoritms must be passed to decode method
            data = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_by_token = uc.get_user_by_username(data["user"])
            if not user_by_token:
                response_maker(1, 401)
        except:
            return response_maker(2, 401)

        return func(user_by_token, *args, **kwargs)
    return decorated

# CRUD with users
# C - Create user
@api.route("/api/v1/register_user", methods = ["POST"])
def register_user():
    """ user API registration route """
    json_data = request.get_json()
    user = {
            "first_name":json_data["first_name"],
            "last_name":json_data["last_name"],
            "username":json_data["username"],
            "password":json_data["password"],
            "password_to_match":json_data["password_to_match"]
        }
    # check if data valid
    errors = validator.validate_registration_data(user)
    if len(errors) > 0:
        return jsonify({ "user_registration_errors": errors }, 406)
    # if data valid - add user to database
    uc.register_user(user)
    return response_maker(8, 200)
# Login user and create token
@api.route("/api/v1/login", methods = ["POST"])
def login():
    """ user API login route """
    json_data = request.get_json()
    username = json_data["username"]
    password = json_data["password"]

    # check if data valid
    errors = validator.validate_login_data(username, password)
    if len(errors) > 0:
        return jsonify({ "error": errors })
    # jwt.encode({ "payload": payload, "exp": expire_time }, secret_key, algorithm="")
    # payload - user identification
    # exp - expire time (if needed)
    # secret_key - secret key for algorithm
    # algorithm - encoding algorithm (default HS256)

    # if data valid - return user token
    token = jwt.encode({"user": username}, SECRET)
    return response_maker(3, 200, "token", token)
# CRUD operations with to-do items
# C - Create to-do
@api.route("/api/v1/add_todo", methods = ["POST"])
@token_validation
def add_todo(user_by_token):
    """ Add to-do - API route """
    description = request.get_json()["description"]
    tc.add_todo(description, user_by_token.id)
    return response_maker(7, 200)
# R - Get to-do list by user id
@api.route("/api/v1/todo_list", methods = ["GET"])
@token_validation
def get_todo_list(user_by_token):
    """ Get to-do list by user id - API route """
    return jsonify({ "todo_list": tc.get_todo_list(user_by_token.id) })
# U - Update to-do status by its id (make it done)
@api.route("/api/v1/update_todo_status", methods = ["POST"])
@token_validation
def update_todo_status(user_by_token):#pylint: disable=W0613
    """ Update to-do list item by id - API route """
    todo_id = request.get_json()["todo_id"]
    # Maybe we can test, if todo belongs to user, who's removing it. (user.id == todo.user_id)
    if not tc.update_todo(todo_id):
        return response_maker(5, 404)
    return response_maker(4, 200)
# D - Remove to-do by its id
@api.route("/api/v1/remove_todo", methods = ["POST"])
@token_validation
def remove_todo(user_by_token):#pylint: disable=W0613
    """ Remove to-do item by id - API route """
    todo_id = request.get_json()["todo_id"]
    # Maybe we can test, if todo belongs to user, who's removing it. (user.id == todo.user_id)
    if not tc.remove_todo(todo_id):
        return response_maker(5, 404)
    return response_maker(6, 200)
