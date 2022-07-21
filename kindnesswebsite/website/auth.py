### pages of the website
from math import fabs
from flask import Blueprint, render_template
from sqlalchemy import false, true

auth = Blueprint("auth", __name__)


@auth.route('/login')
def login():
    # add variables (as many as you want)
    return render_template("login.html", text="Testing", usr="Peter", isTrue=True)


@auth.route('/logout')
def logout():
    return "<p> Logout </p>"


@auth.route('/sign-up')
def sign_up():
    return render_template("sing_up.html")





