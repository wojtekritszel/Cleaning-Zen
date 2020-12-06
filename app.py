from flask import Flask, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = 'QtkglpwWstret1_12'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # dodane by obsłużyć błąd SQLALCHEMY_TRACK_MODIFICATIONS warning


bootstrap = Bootstrap(app)
moment = Moment(app)

db = SQLAlchemy(app)


"""Klasy formularzy"""


class NameForm(FlaskForm):
    name = StringField('Jak masz na imię?', validators=[DataRequired()])
    submit = SubmitField('Wyślij')


class ItemName(FlaskForm):
    name = StringField('Nazwa przedmiotu', validators=[DataRequired()])
    description = StringField('Opis przedmiotu')
    purchase_date = DateField('Data zakupu')
    condition = IntegerField('Stan w skali 1-10')
    submit = SubmitField('Wyślij')


class ContainerName(FlaskForm):
    name = StringField('Nazwa pojemnika', validators=[DataRequired()])
    description = StringField('Opis pojemnika')
    place = StringField('Miejsce przechowywania')
    insert = StringField('Zawartość')
    submit = SubmitField('Wyślij')


""" Klasy bazy danych """


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    condition = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'), nullable=False)
    container = db.relationship("Container", backref=db.backref('items', lazy=True))

    def __repr__(self):
        return '<Item %r>' % self.name


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Container %r>' % self.name


@app.errorhandler(400)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')     # kod, który powoduje, że przy odświerzaniu strony nie pojawia się komunikat o wysłaniu nowego formularza
        if old_name is not None and old_name != form.name.data:
            flash('Wygląda na to, że teraz nazywasz się inaczej!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/items', methods=['GET', 'POST'])
def form_add_item():
    itemform = ItemName()
    session['item'] = itemform.name.data
    return render_template('form_add_item.html', form=itemform, name=session.get('item'))


@app.route('/container', methods=['GET', 'POST'])
def form_add_container():
    containerform = ContainerName()
    session['container'] = containerform.name.data
    return render_template('form_add_container.html', form=containerform, name=session.get('container'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == "__main__":
    db.init_app(app)
    db.create_all()
    app.run(debug=True)
