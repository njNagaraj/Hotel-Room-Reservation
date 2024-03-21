from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from Hotel_Reservation.models import Customer

class ReservationForm(FlaskForm):
  guest_name = StringField('Guest Name', validators=[DataRequired()])
  check_in_date = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
  check_out_date = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
  room_id = HiddenField('Room ID', validators=[DataRequired()])
  submit = SubmitField('Make Reservation')