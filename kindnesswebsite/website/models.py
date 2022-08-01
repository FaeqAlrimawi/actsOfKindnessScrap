from sqlalchemy import PrimaryKeyConstraint
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import enum

class ActType(enum.Enum):
        NORMAL= "Normal Act"
        ANTI_SOCIAL = "Anit-Social Act"
        
        
## class for the notes that a user creates
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # class name des not need to be capitalised
       
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # link a user to their notes (need to capitalise the name of the calss)
    acts = db.relationship('AoK')
    non_aok_acts = db.relationship('NonAoK')
    
    
class AoK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class NonAoK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.column(db.Enum(ActType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    
    