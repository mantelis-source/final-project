from sqlalchemy import (Integer, String)
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from .. import db

class User(db.Model, UserMixin):
    """ User model. Object to create and make manipulations with database """
    # table name in database
    __tablename__ = "users"
    
    # id - user id as primary key
    id = db.Column("id", Integer, primary_key=True, nullable=False)
    # public id - used to hide real users number, or other relevant data about database
    public_id = db.Column("public_id", String(100), unique=True, nullable=False)
    # users first name
    first_name = db.Column("firstname", String(50))
    # users last name
    last_name = db.Column("lastname", String(50))
    # users username (login). Must be unique.
    username = db.Column("username", String(100), unique=True)
    # password - hashed
    password = db.Column("password", String(200))
    # relationship with Todo table
    todo_list = relationship("Todo")
    
    def __init__(self, public_id,firs_name, 
                 last_name, username, password):
        """ Initialize model """
        
        self.public_id = public_id
        self.first_name = firs_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def to_json(self):
        """ method used to convert model data to json """
        return {
                "id": self.id,
                "public_id": self.public_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "user_name": self.username,
                "password": self.password
                }