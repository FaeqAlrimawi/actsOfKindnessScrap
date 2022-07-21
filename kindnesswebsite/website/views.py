### pages of the website
from flask import Blueprint, render_template

views = Blueprint("views", __name__)


# the route of our website
@views.route('/')
def home():
    return render_template("home.html")



