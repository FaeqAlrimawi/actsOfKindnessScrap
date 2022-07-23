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

file_name = './website/static/actsOfKindness.xlsx'
# file_name = 'actsOfKindness.xlsx'
sheet_name = 'All_AoKs'
description_column = 'Description'


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
 
    df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])
    return render_template("listofAoK.html", acts=df.values, user=current_user)
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


# @views.route("/api/data")
# def data():
    # # query = request.query_string
    
    # df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])[0:100]
    # # print("#### ",query)

    # # # search filter
    # search = request.args.get('search[value]')
    # if search:
    #     df = df.apply(lambda row: row.astype(str).str.contains(f'%{search}').any(), axis=1)
    
    # total_filtered = df.count()
    # # print("#### ", df)
    # # total_filtered = query.count()

    # # # sorting
    # # order = []
    # # i = 0
    # # while True:
    # #     col_index = request.args.get(f'order[{i}][column]')
    # #     if col_index is None:
    # #         break
    # #     col_name = request.args.get(f'columns[{col_index}][data]')
    # #     if col_name not in ['Description']:
    # #         col_name = 'Description'
    # #     descending = request.args.get(f'order[{i}][dir]') == 'desc'
    # #     col = getattr(df, col_name)
    # #     if descending:
    # #         col = col.desc()
    # #     order.append(col)
    # #     i += 1
    # # if order:
    # #     query = query.order_by(*order)

    # # # pagination
    # # start = request.args.get('start', type=int)
    # # length = request.args.get('length', type=int)
    # # query = df.offset(start).limit(length)
    
    
    # # print(df.values)
    # # response
    # return {
    #     # 'data': [user.to_dict() for user in query],
    #     'recordsFiltered': total_filtered,
    #     # 'recordsTotal': query.count(),
    #     # 'draw': request.args.get('draw', type=int),
    #     'data' : [df.to_json()],
    # }





