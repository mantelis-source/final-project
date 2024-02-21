from sqlalchemy import (
    Integer, 
    String, 
    Boolean,
    DateTime,
    ForeignKey)
from flask_login import UserMixin
from .. import db
from datetime import datetime


class Todo(db.Model, UserMixin):
    """ Todo model. Object to create and make manipulations with database """
    # table name in database
    __tablename__ = "todos"
    # id - needs a primary key 
    id = db.Column("id", Integer, primary_key=True, nullable=False)
    # to-do descriptio - to-do text
    description = db.Column("description", String(200))
    # is to-do done, o only created
    is_done = db.Column("isdone", Boolean)
    # creation date and time
    created_date = db.Column("created_date", DateTime)
    # date, when todo was set as done
    done_date = db.Column("done_date", DateTime)
    # user id to create relationship with User model
    user_id = db.Column("user_id", Integer, ForeignKey("users.id"))
    
    def __init__(self, description, user_id):
        """ Initialize model """
        creation_date = datetime.strptime(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"%Y-%m-%d %H:%M:%S") 
        
        self.description = description
        self.is_done = False
        self.created_date = creation_date
        self.user_id = user_id
    
    def to_json(self):
        """ method used to convert model data to json """
        return {
                "id": self.id,
                "description": self.description,
                "is_done": self.is_done,
                "created_date": self.created_date,
                "done_date": self.done_date
                }