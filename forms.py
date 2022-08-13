from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    gnere = StringField('gnere', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])

class AuthorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])