from flask_wtf import FlaskForm
from wtforms import StringField, TimeField
from wtforms.validators import DataRequired

class AuthorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])

class BookForm(FlaskForm):
    book_title = StringField('book_title', validators=[DataRequired()])
    genre = StringField('genre', validators=[DataRequired()])
    year = TimeField('year', validators=[DataRequired()])