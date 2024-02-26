""" This file is used to make most common actions """
import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """ using onw method to create application"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('flask_secret_key')
    app.config["SQLALCHEMY_DATABASE_URI"] = \
    f'mysql+pymysql://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_host')}/{os.getenv('db_name')}'
    db.init_app(app)

    from .views import views    #pylint:disable=C0415
    from .api import api    #pylint:disable=C0415
    # register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(api, url_prefix="/")

    from .models.user import User #pylint:disable=C0415
    from .models.todo import Todo #pylint:disable=C0415
    # creating database schema
    with app.app_context():
        db.create_all()
    # login_manager initialization
    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """ default load_user method """
        return User.query.get(id)

    return app
