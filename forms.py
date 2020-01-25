from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
import states


class AddressForm(FlaskForm):
    street = StringField('Street Number')
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip (5 Digit)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StateForm(FlaskForm):
    state = SelectField('',
                        choices=[(s['alpha'], s['name']) for s in states.states])
    submit = SubmitField('Submit')



