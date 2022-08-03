from sqlalchemy import PrimaryKeyConstraint
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
# from sqlalchemy import Enum
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
    non_aok_acts = db.relationship('NonAok')
    
    
class Aok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    source = db.Column(db.String(1000))
    categories = db.relationship('AokCategories', cascade = 'all, delete-orphan', lazy = 'dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nlp_models = db.relationship('ModelAok', cascade = 'all, delete-orphan', lazy = 'dynamic')
    
    
    

class NonAok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.Enum(ActType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nlp_models = db.relationship('ModelNonAok', cascade = 'all, delete-orphan', lazy = 'dynamic')
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    acts = db.relationship('AokCategories', cascade = 'all, delete-orphan', lazy = 'dynamic')
    

## association table between categories and aok showing which aoks belong to which categories      
class AokCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  
    aok_id =  db.Column(db.Integer, db.ForeignKey('aok.id'))
      
    
class NLPModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    model = db.Column(db.PickleType)
    features = db.Column(db.PickleType)
    aoks = db.relationship('ModelAok', cascade = 'all, delete-orphan', lazy = 'dynamic')
    non_aoks = db.relationship('ModelNonAok', cascade = 'all, delete-orphan', lazy = 'dynamic')
    

## association table between models and aok showing which aoks belong to which models    
class ModelAok(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    aok_id =  db.Column(db.Integer, db.ForeignKey('aok.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('nlp_model.id'))
    

## association table between models and non-aok showing which non-aoks belong to which models    
class ModelNonAok(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    non_aok_id =  db.Column(db.Integer, db.ForeignKey('non_aok.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('nlp_model.id'))
        
    
     
    
    