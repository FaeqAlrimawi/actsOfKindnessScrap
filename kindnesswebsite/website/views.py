### pages of the website
import pandas as pd
from flask import Blueprint, render_template
import os

views = Blueprint("views", __name__)


# the route of our website
@views.route('/')
def home():
    return render_template("home.html")


@views.route('/guessAoK')
def guessAoK():
    return render_template("guessAoK.html")



@views.route('/listofAoK')
def listofAoK():
    file_name = './website/static/actsOfKindness.xlsx'
    # file_name = 'actsOfKindness.xlsx'
    sheet_name = 'All_AoKs'
    description_column = 'Description'

    df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])
    return render_template("listofAoK.html", tableHtml=df.to_html())
    # return df.to_html()