from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from states import States


class AddressForm(FlaskForm):
    street = StringField('Street Number')
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip (5 Digit)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StateForm(FlaskForm):
    state = SelectField('',
                        choices=[(s['alpha'], s['name']) for s in States.states])
    submit = SubmitField('Submit')



