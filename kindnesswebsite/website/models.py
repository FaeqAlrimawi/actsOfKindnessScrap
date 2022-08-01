from sqlalchemy import PrimaryKeyConstraint
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import enum

class ActType(enum.Enum):
        NORMAL= "Normal Act"
        ANTI_SOCIAL = "Anit-Social Act"
            
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    acts = db.relationship('Aok') # link a user to their aoks (need to capitalise the name of the calss)
    non_aok_acts = db.relationship('Non_aok')
    
    
class Aok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    categories = db.relationship('Aok_Categories')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    

class Non_aok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.column(db.Enum(ActType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    acts = db.relationship('Aok_Categories')
    
    
class Aok_Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  
    aok_id =  db.Column(db.Integer, db.ForeignKey('aok.id'))
      
    
     
    