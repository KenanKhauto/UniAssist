
from flask import render_template
from flask import Blueprint
from application.extensions import mongo

main = Blueprint('main', __name__)

@main.route("/")
def home():
    docs = mongo.db.test.find()
    return render_template("home.html", docs = docs)