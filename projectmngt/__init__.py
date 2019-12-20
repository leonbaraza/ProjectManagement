from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from projectmngt.config.config import Config


# app.config.from_envvar('APP_SETTINGS')

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.Login'


# creating a function of your app

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from projectmngt.users.routes import users
    from projectmngt.project.routes import projects
    from projectmngt.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(projects)
    app.register_blueprint(main)

    return app

