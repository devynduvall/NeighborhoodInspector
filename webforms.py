from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

class LoginForm(FlaskForm):
    username = StringField("What's Your Username", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	# favorite_color = StringField("Favorite Color")
	# about_author = TextAreaField("About Author")
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	# profile_pic = FileField("Profile Pic")
	submit = SubmitField("Submit")
      

class FilteringForm(FlaskForm):
    restaurant_cuisine = SelectMultipleField(u'Cuisine Preference', choices=[('all', 'All'),('coffee_shop', 'Coffee Shop'), ('pizza', 'Pizza')])
    submit = SubmitField("Submit")
