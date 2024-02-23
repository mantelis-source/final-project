import uuid
import bcrypt
from ..models.user import User
from .. import db

def login_user(username, password):
    """ method to check login data """
    user = User.query.filter_by(username=username).first()
    if user:
        if bcrypt.checkpw(str(password).encode("utf-8"), str(user.password).encode("utf-8")):
            return user
    return None

def register_user(user_info):
    """ method to register (add) user to database"""
    password = str(user_info["password"]).encode("utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    user = User(str(uuid.uuid4()),
                user_info["first_name"], 
                user_info["last_name"], 
                user_info["username"],
                hashed_password)
    
    db.session.add(user)
    db.session.commit()
    
def get_user_by_username(username):
    """method to get user by username"""
    return User.query.filter_by(username=username).first()
