### pages of the website
from operator import methodcaller
import pandas as pd
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
import os
from flask_login import login_required, current_user
from . import db
from .models import AoK
import json
from .control import checkIfAoK


views = Blueprint("views", __name__)


# the route of our website
@views.route('/', methods=['GET', 'POST'])
def home():
    
    # if request.method == 'POST':
    #     aok = request.form.get('aok')
        
    #     if len(aok)<1:
    #         flash("Act too short!", category='error')
    #     else:
    #         new_aok = AoK(act=aok, user_id=current_user.id)
    #         db.session.add(new_aok)
    #         db.session.commit()
    #         flash("Act added successfully", category='success')
    return render_template("home.html", user=current_user)


@views.route('/guessAoK', methods=['POST', 'GET'])
def guessAoK():

    if request.method == 'POST':
        act = request.form.get('act')
        
        if act:
           probability = checkIfAoK(act)
               
           return render_template('guessAoK.html', user=current_user, prob=probability, act=act)
        else:
            flash("Please enter an act", category='error')

            
    return render_template("guessAoK.html", user=current_user, prob=-1, act="")


@views.route('/edit', methods=['GET', 'POST'])
def editAoK():
    
    if request.method == 'POST':
        aok = request.form.get('aok')
        
        if len(aok)<1:
            flash("Act too short!", category='error')
            
        else:
            new_aok = AoK(act=aok, user_id=current_user.id)
            db.session.add(new_aok)
            db.session.commit()
            
            flash("Act added successfully", category='success')
            
    return render_template("editAoK.html", user=current_user)



@views.route('/listofAoK')
def listofAoK():
    file_name = './website/static/actsOfKindness.xlsx'
    # file_name = 'actsOfKindness.xlsx'
    sheet_name = 'All_AoKs'
    description_column = 'Description'

    df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])
    return render_template("listofAoK.html", tableHtml=df.to_html(), user=current_user)
    # return df.to_html()
    
    
@views.route('/delete-AoK', methods=['POST'])
def delete_AoK():
    aok = json.loads(request.data)
    aokId = aok['aokId']      
    
    aok = AoK.query.get(aokId)
    if aok.user_id == current_user.id:
        db.session().delete(aok)
        db.session.commit()
        
    return jsonify({})

