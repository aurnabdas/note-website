from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_required


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Joe MAMA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'#just says that database is located in the website folder 
    db.init_app(app)#this is the app we are going to use with this database


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note
    #we wont actually use anything, we need to make sure we load the file(model.py) before we create our database
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #this is where the user will be redirecred if they are not logged in 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #this is telling flask how we load in user # btw .get always looks for the primary key


        

    return app

# def create_database(app): #will check if the database exist, if not it will create it 
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=all)# this is what creates the dabase
#         print('Created Database!')
# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')