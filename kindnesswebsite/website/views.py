### pages of the website
from flask import Blueprint

views = Blueprint("views", __name__)


# the route of our website
@views.route('/')
def home():
    return "<h1> HOME </h1"



