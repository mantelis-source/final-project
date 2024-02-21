from .. import db
from ..models.todo import Todo
from datetime import datetime

def add_todo(description, user_id):
    """ method to add to-do to database """
    todo = Todo(description, user_id)
    
    db.session.add(todo)
    db.session.commit()

def remove_todo(id):
    """ method to remove to-do from database"""
    todo = Todo.query.get(id)
    if not todo:
        return False
    else:
        db.session.delete(todo)
        db.session.commit()
    
    return True

def update_todo(id):
    """ method to update to-do status (is_done set to True)"""
    todo = Todo.query.get(id)
    done_date = datetime.strptime(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"%Y-%m-%d %H:%M:%S") 
    if not todo:
        return False
    else:
        db.session.query(Todo).filter_by(id = id).update({ 'is_done': True, 'done_date': done_date} )
        db.session.commit()
    
    return True

def get_todo_list(user_id):
    """ method to return to-do list from database by user id"""
    todos = Todo.query.filter_by(user_id = user_id).all()
    json_list = []
    for todo in todos:
        json_list.append(todo.to_json())
    return json_list