from flask import Flask
from .extensions import mongo
from .routes.routes import main

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9b1b6efaadc4821aa8dbc985588acb28'
    app.config['MONGO_URI'] = 'mongodb+srv://kenan:Yyecgaa123123@cluster0.s0aykgz.mongodb.net/UniAssistDB?retryWrites=true&w=majority'
    mongo.init_app(app)
    app.register_blueprint(main)

    return app
