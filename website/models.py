from . import db #importing dc from the init file
from flask_login import UserMixin
from sqlalchemy.sql import func



#the db.model is being inherted. it is a layout for an object that will be stored in the database. 
#you are telling the program that all Users and notes must follow these rules that are being set in these two classes
class Note(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    #func is what stores the actual current date and time. func is imported from sqlalchemy

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    #foreign key is a key of one of your database tables that refernces an id to another database column
    #the first parameter repersents what type of value the column is going to be. in this case a integer
    #the 'user.id' is the User class defined above and it is grabbing the unquie id of that user
    #user_id is unqie because it has a one to many relationship, as in one user can have many notes. this is a database terminlogy. there is also many to one, for example one note to many users. there is also one to one


    #if you want to add more thigns to to website check out 1:28:30 on the video
    #also you can check flash sqlalchemy documentation

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True) 
    # unique makes it so users cannot have the same email
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #every time a user creates a note the db.relationship(a list) stores all of the differnt notes
    