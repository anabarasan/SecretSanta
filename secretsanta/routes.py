import json
import random

from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests
from sqlalchemy import and_

from secretsanta import app, db
from secretsanta.forms import LoginForm, RegistrationForm, ChildSelectForm, MessageForm
from secretsanta.models import User


MESSAGE = '''{}

with love,

Mom'''

WALLPAPERS = [                                                                                                                                
    'christmas_12.jpg',                                                                                                                       
    'Christmas-Cookies-Full.jpg',                                                                                                             
    'Christmas-Cookies.jpg',                                                                                                                  
    'Christmas-Decoration-Patterb.jpg',                                                                                                       
    'Christmas-Decorations.jpg',                                                                                                              
    'Christmas-Lights.jpg',                                                                                                                   
    'Christmas-tree.jpg',                                                                                                                     
    'Firefox.png',                                                                                                                            
    'game-of-thrones.jpg',                                                                                                                    
    'golden-christmas-stars.jpg',                                                                                                             
    'merry_christmas.jpg',                                                                                                                    
    'red-christmas.jpg',                                                                                                
    'santa-claus-flying.jpg',                                                                                           
    'small-christmas-house.jpg',                                                                                        
    'StarWars.jpg',                                                                                                     
    'superheroes-christmas.jpg',                                                                                        
    'tangle-of-christmas-lights.jpg',                                                                                   
]

def get_wallpaper_filename():
    filename = random.choice(WALLPAPERS)
    return url_for('static', filename=filename)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    me = User.query.filter_by(username=current_user.username).first()
    if me.child is None:
        return redirect(url_for('configure_child'))
    form = MessageForm()
    if form.validate_on_submit():
        child_name = me.child.username
        message = app.config['WEBHOOK_MESSAGE'].format(form.message.data)
        response = requests.post(
            url=app.config['TEAMS_WEBHOOK'],
            data=json.dumps({
                "title": "{}'s mommy says".format(child_name),
                "text": message
            })
        )
        # print(response.status_code)
        # print(response.text)
        response.raise_for_status()
        return redirect(url_for('index'))
    return render_template('index.html', title='Send Message', form=form, wallpaper=get_wallpaper_filename())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, wallpaper=get_wallpaper_filename())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, wallpaper=get_wallpaper_filename())

@app.route('/configurechild', methods=['GET', 'POST'])
@login_required
def configure_child():
    me = User.query.filter_by(username=current_user.username).first()
    choices = []
    if me.child is None:
        all_users = User.query.all()
        allocated_users = []
        for user in all_users:
            if user.offspring:
                allocated_users.append(user.offspring)
        other_users = User.query.filter(
            and_(User.username!=current_user.username, User.id.notin_(allocated_users))).all()
        for user in other_users:
            choices.append((user.id, user.email))
    form = ChildSelectForm()
    form.child.choices = choices
    if form.validate_on_submit():
        selected_child = User.query.filter_by(id=form.child.data).first()
        me.child = selected_child
        db.session.add(me)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addchild.html', title='Select Child', form=form, user=me, wallpaper=get_wallpaper_filename())