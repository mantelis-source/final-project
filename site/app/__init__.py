from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# initialize SQLAlchemy object to 
# communication with database
db = SQLAlchemy()
DB = "my.db"

def createApp():
    """ using onw method to create application"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sdfsdfs"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB}'
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
    