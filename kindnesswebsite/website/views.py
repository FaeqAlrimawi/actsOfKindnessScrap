### pages of the website
from operator import methodcaller
import pandas as pd
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
import os
from flask_login import login_required, current_user
from . import db
from .models import Note
import json
from .control import checkIfAoK


views = Blueprint("views", __name__)


# the route of our website
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note)<1:
            flash("Act too short!", category='error')
        else:
            new_note  =Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Act added successfully", category='success')
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



@views.route('/listofAoK')
def listofAoK():
    file_name = './website/static/actsOfKindness.xlsx'
    # file_name = 'actsOfKindness.xlsx'
    sheet_name = 'All_AoKs'
    description_column = 'Description'

    df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])
    return render_template("listofAoK.html", tableHtml=df.to_html(), user=current_user)
    # return df.to_html()
    
    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']      
    
    note = Note.query.get(noteId)
    if note.user_id == current_user.id:
        db.session().delete(note)
        db.session.commit()
        
    return jsonify({})

