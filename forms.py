from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddressForm(FlaskForm):
    street = StringField('Street Number')
    city = StringField('City')
    state = StringField('State', validators=[DataRequired()])
    zip = IntegerField('Zip (5 Digit)')
    submit = SubmitField('Submit')
