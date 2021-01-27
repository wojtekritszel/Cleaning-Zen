from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, DateField, SelectField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('Jak masz na imię?', validators=[DataRequired()])
    submit = SubmitField('Wyślij')


class ItemName(FlaskForm):
    name = StringField('Nazwa przedmiotu', validators=[DataRequired()])
    description = StringField('Opis przedmiotu')
    purchase_date = DateField('Data zakupu')
    condition = SelectField('Stan w skali 1-10', choices=[('tragiczny - 1'), ('mocno zniszczony - 2'),
                                                          ('zniszczony - 3'), ('znoszony - 4'), ('ślady użytkowania - 5'),
                                                          ('przeciętny - 6'), ('dobry - 7'), ('bardzo dobry - 8'),
                                                          ('idealny - 9'), ('nowy - 10')])
    image = FileField('Zdjęcie przedmiotu')
    submit = SubmitField('Wyślij')


class ContainerName(FlaskForm):
    name = StringField('Nazwa pojemnika', validators=[DataRequired()])
    description = StringField('Opis pojemnika')
    place = StringField('Miejsce przechowywania')
    insert = StringField('Zawartość')
    submit = SubmitField('Wyślij')


