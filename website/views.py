from flask import Blueprint, jsonify, render_template, request, flash, jsonify 
from flask_login import login_required, current_user
from .models import Note
from . import db
import json



views = Blueprint("views", __name__)


@views.route("/", methods = ['GET', 'POST'])
@login_required #this requires you to be logged in to see home page
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('note is to small', category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note add', category='success')
    return render_template("home.html", user=current_user) #user=current_suer lets us refernce current user from our template, and check if it is authenitcated

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #it is going to take request.data which is a string, and turn it into a python dictionaly object so we can access the note id 
    noteId = note['noteId']
    note = Note.query.get(noteId) #NOTE that get access's the primart key of the item
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
