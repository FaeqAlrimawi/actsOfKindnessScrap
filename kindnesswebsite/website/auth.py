### pages of the website
from math import fabs
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import false, true
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # data = request.form
    # print(data)
    # add variables (as many as you want)
    return render_template("login.html", text="Testing", usr="Peter", isTrue=True)


@auth.route('/logout')
def logout():
    return "<p> Logout </p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    
    if request.method == 'POST':
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
    
        #check data
        if len(email)<4:
            ##categories are up to us
            flash("Email should be greater than 4 chars", category='error')
        elif len(firstName) < 3:
            flash("name should be greater than 2 chars", category='error')
        elif len(password1) < 7:
            flash("password should be greater than 7 chars", category='error')
        elif password1 != password2:
            flash("passowrds do not match", category='error')
        else:
            #add user to databse
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success') 
            return redirect(url_for('views.home'))
    
    return render_template("sing_up.html")





