### pages of the website
import pandas as pd
from flask import Blueprint, render_template


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
    file_name = '/static/actsOfKindness.xlsx'
    sheet_name = 'Adams Media'
    description_column = 'Description'

    df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])
    # return render_template("listofAoK.html")
    return df.to_html()