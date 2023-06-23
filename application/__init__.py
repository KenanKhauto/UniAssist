
from flask import Flask
from .extensions import mongo, login_manager, bcrypt
from .main.routes import main
from .users.routes import users

def create_app():


    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9b1b6efaadc4821aa8dbc985588acb28'
    app.config['MONGO_URI'] = 'mongodb+srv://kenan:Yyecgaa123123@cluster0.s0aykgz.mongodb.net/UniAssistDB?retryWrites=true&w=majority'

    mongo.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(users)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "main.login"  # this is what we pass for @login_required
    login_manager.login_message_category = "info"


    return app

 