from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from Hotel_Reservation.models import Customer

class SignUpForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  # Custom validation for username
  def validate_username(self, username):
      existing_user = Customer.query.filter_by(username=username.data).first()
      if existing_user:
          raise ValidationError('Username already exists. Please choose a different username.')

  # Custom validation for email
  def validate_email(self, email):
      existing_email = Customer.query.filter_by(email=email.data).first()
      if existing_email:
          raise ValidationError('Email already exists. Please choose a different email.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')