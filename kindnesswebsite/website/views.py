### pages of the website
from operator import methodcaller
from numpy import result_type
import pandas as pd
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for, Markup, session
import os
from flask_login import login_required, current_user
from . import db
from .models import AoK
import json
from .control import canScrap, checkIfAoK, doesAoKExist, getRobotsURL, scrapWebsite, addAoK
import website


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
        
        print("#### ", act)
        if act:
           probability = checkIfAoK(act)
        #    d =  jsonify(prob=probability) 
        #    print("wwwww ", probability)
        #    return d   
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


@views.route('/add-AoK', methods=['POST'])
def add_AoK():
    # print("##### in add aok")
    aok = json.loads(request.data)
    aok_str = aok['aok']   
    
    if type(aok_str) != str:
        aok_str = str(aok_str)
          
                    
    # check if already exists in the database
    inDB = doesAoKExist(aok_str)
    
    if inDB:
        result = jsonify({'message':'exists'})
        # print(result.data)
        return result
    else: 
        result = addAoK(aok_str) 
        if result:
            
            res = {'message':'added'} 
            return jsonify(res)
        else:
            return jsonify({'message':'error'})


@views.route('/update-prob', methods=['POST'])
def update_prob():
     aok = json.loads(request.data)
     aok_str = aok['aok']
     
     if type(aok_str) != str:
        aok_str = str(aok_str)
        
     prob = checkIfAoK(aok_str)  
     
     return jsonify({'prob':prob}) 
        
        
    
    
@views.route("/aok-scrapper", methods=["POST", "GET"])
def aokScrapper():
    
    if request.method == 'POST':
        # data = json.loads(request.data)
        # websiteURL = data['websiteURL']         
        # sentences = scrapWebsite(websiteURL)
        # act_probs = []
        
        # if sentences:
        #     for sent in sentences:

        #         prob = checkIfAoK(sent)
        #         pair = {'act':sent, 'prob':prob}
        #         act_probs.append(pair)
        
            
        # # return render_template("scrapper.html", user=current_user, websiteURL=websiteURL, act_probs=act_probs, canScrap=True)
        # isPer = canScrap(websiteURL)
        
        # if( not isPer):
        #    robotUrl = getRobotsURL(websiteURL)
        #    flash(Markup("Scraping may not be permissible on this webpage per the website's permissions. For more info, see: <a href=\""+robotUrl+"\" target='_blank' class=\"alert-link\">"+robotUrl + "</a>") , category='warning')
        # # print(json.dumps(act_probs))
        # return jsonify({"result":"success", "acts":json.dumps(act_probs)});    
        websiteURL = request.form.get('websiteURL')         
        sentences = scrapWebsite(websiteURL)
        act_probs = []
        
        if sentences:
            for sent in sentences:

                prob = checkIfAoK(sent)
                pair = (sent, prob)
                act_probs.append(pair)
        
            
        # return render_template("scrapper.html", user=current_user, websiteURL=websiteURL, act_probs=act_probs, canScrap=True)
        isPer = canScrap(websiteURL)
        
        if( not isPer):
           robotUrl = getRobotsURL(websiteURL)
           flash(Markup("Scraping may not be permissible on this webpage per the website's permissions. For more info, see: <a href=\""+robotUrl+"\" target='_blank' class=\"alert-link\">"+robotUrl + "</a>") , category='warning')
            
        return render_template("scrapper.html", user=current_user, websiteURL=websiteURL, robotsURL=getRobotsURL(websiteURL), act_probs=act_probs) 
    
    return render_template("scrapper.html", user=current_user)



@views.route("/aok-model", methods=["POST", "GET"])
def AoKModel():
    return render_template("AoKModel.html", user=current_user)
  
  
    
@views.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))


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





