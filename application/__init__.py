from flask import Flask
from .extensions import mongo
from .routes.routes import main

def create_app():

    app = Flask(__name__)

    app.config['MONGO_URI'] = 'mongodb+srv://kenan:Yyecgaa123123@cluster0.s0aykgz.mongodb.net/UniAssistDB?retryWrites=true&w=majority'
    mongo.init_app(app)
    app.register_blueprint(main)

    return app
