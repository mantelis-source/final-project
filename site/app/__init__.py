""" This file is used to make most common actions """
import boto3
import json
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#def get_secrets():
#    client = boto3.client('secretsmanager', region_name='eu-central-1')
#    response = client.get_secret_value(SecretId='db_creds')
#    secrets = json.loads(response['SecretString'])
#    return secrets
# initialize SQLAlchemy object to
# communication with database
db = SQLAlchemy()
#aws_secrets = get_secrets()

def create_app():
    """ using onw method to create application"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sdfsdgsdfg"#""aws_secrets['flask_secret_key']
#    app.config["SQLALCHEMY_DATABASE_URI"] = \
#    f'mysql+pymysql://{aws_secrets['db_username']}:{aws_secrets['db_password']}@{aws_secrets['db_host']}/{aws_secrets['db_name']}'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my.db"
    db.init_app(app)

    from .views import views
    from .api import api
    # register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(api, url_prefix="/")

    from .models.user import User
    from .models.todo import Todo
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
