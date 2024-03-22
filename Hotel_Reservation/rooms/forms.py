from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired

# Reservation form
class ReservationForm(FlaskForm):
  guest_name = StringField('Guest Name', validators=[DataRequired()])
  check_in_date = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
  check_out_date = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
  room_id = HiddenField('Room ID', validators=[DataRequired()])
  submit = SubmitField('Make Reservation')