from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .validators.validators import Validator
from .controllers import user_controller as uc
from .controllers import todo_controller as tc
from flask_login import login_user, login_required, logout_user, current_user
import json

# create blueprint
views = Blueprint('views', __name__)
# create validator 
validator = Validator()

@views.route("/", methods = ["GET", "POST"])
@login_required
def index():
    """ default route - user login required"""
    if request.method == "POST":
        description = request.form["todo"]
        # tc - todo controller
        tc.add_todo(description, current_user.id)
    # render template and reload
    return render_template("index.html", user_data = current_user)

@views.route("/login", methods = ["GET", "POST"])
def login():
    """ login route used to login the user """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # validate user login data
        errors = validator.validate_login_data(username, password)
        if len(errors) > 0:
            for error in errors:
                # show error
                flash(error, category="error")
            return redirect(url_for("views.login"))
        # if user provided data valid - get user from database and
        # register ir to flask 
        user = uc.login_user(username, password)
        login_user(user)
        return redirect(url_for("views.index"))
    return render_template("login.html")

@views.route("/logout")
@login_required
def logout():
    """ logout route """
    logout_user()
    return redirect("/")

@views.route("/register", methods = ["GET", "POST"])
def register():
    """ route used to register user """
    if request.method == "POST":
        form_data = request.form
        user = {
            "first_name":form_data["first_name"],
            "last_name":form_data["last_name"],
            "username":form_data["username"],
            "password":form_data["password"],
            "password_to_match":form_data["password_to_match"]
            }
        # check if user data is valid
        errors = validator.validate_registration_data(user)
        if len(errors) > 0:
            for error in errors:
                # show errors
                flash(error, category='error')
            return render_template("register.html", user_data = form_data)
        # if data are valid - add user to database
        uc.register_user(user)
        # show message
        flash("Your account has been created successfully.", category='success')
        return redirect(url_for('views.login'))
    return render_template("register.html", user_data = None)

@views.route("/remove-todo", methods=["POST"])
def remove_todo():
    """ method to remove to-do by id from database """
    data = json.loads(request.data)
    todo_id = data["itemId"]
    
    if tc.remove_todo(todo_id):
        return jsonify(success=True)
    return jsonify(success=False)

@views.route("/update-todo", methods=["POST"])
def update_todo():
    """ method to update to-do by id in database """
    data = json.loads(request.data)
    todo_id = data["itemId"]
    
    if tc.update_todo(todo_id):
        return jsonify(success=True)
    return jsonify(success=False)