
import os
from flask import Flask
from .extensions import mongo, login_manager, bcrypt
from .main.routes import main
from .users.routes import users
from .post.routes import post

def create_app():


    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

    mongo.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(post)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "main.login"  # this is what we pass for @login_required
    login_manager.login_message_category = "info"


    return app

 