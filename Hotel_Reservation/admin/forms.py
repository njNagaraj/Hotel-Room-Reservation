from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class AdminLoginForm(FlaskForm):
  username = StringField('Admin Username', validators=[DataRequired()])
  password = PasswordField('Admin Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class AddRoomForm(FlaskForm):
  room_number = StringField('Room Number', validators=[DataRequired()])
  amenities = StringField('Amenities', validators=[DataRequired()])
  capacity = IntegerField('Capacity (Number of Guests)', validators=[DataRequired(), NumberRange(min=1)])

class EditRoomForm(FlaskForm):
  room_number = StringField('Room Number', validators=[DataRequired()])
  amenities = StringField('Amenities', validators=[DataRequired()])