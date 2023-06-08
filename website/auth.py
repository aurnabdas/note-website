
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)#this will login the user with the email that is present in the database, remember makes sures the user is logged in until the user logs out or in other words when the user clears the session
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #make sures that the person is already logged in before accessing this page
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        user = User.query.filter_by(email=email).first()

        if user:#this is a check to see if the email is already in the database
            flash('this email already exists', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4", category='error')
        elif len(first_name) < 2:
            flash("First Name must be greater than 2", category='error')

        elif password1 != password2:
            flash("Password's are not the same", category='error')

        elif len(password1) < 3:
            flash("Password must be greater than 8", category='error')

        else:
            # add user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit() #this causes an Operational Error, otherwise it works 
            login_user(new_user, remember=True)
            flash("HOORAY", category='success')
            return redirect(url_for('views.home'))
            # after you sign the user up you will redirect them to the home page.
            # you can also do return redirect("/"), but what i wrote is better because in the scenrio you change the root name to / to something else you will not need to change the code above



    return  render_template("sign_up.html", user=current_user)



