from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Email
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

def email_check_missing_at(form, field): 
    if form.name.data is None: 
        return
    first_name = form.name.data.split()[0]
    message = f"Please include an '@' in the email address. '{first_name}' is missing an '@'."
    if first_name.lower() == field.data.lower():
        raise ValidationError(message)
    
class UserInfoForm(FlaskForm):
    name = StringField('What is your name?', validators=[InputRequired()])
    email = StringField('What is your UofT email address?', validators=[InputRequired(), email_check_missing_at])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserInfoForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        if 'utoronto' in form.email.data:
            session['is_uoft_email'] = True
        else: 
            session['is_uoft_email'] = False
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), is_uoft_email=session.get('is_uoft_email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.now(timezone.utc))