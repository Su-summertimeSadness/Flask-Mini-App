from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,  SubmitField
from wtforms.validators import DataRequired




class UserForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField()