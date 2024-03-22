from Hotel_Reservation import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

# customer db model
class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

#room db model
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    reservations = db.relationship('Reservation', backref='room', lazy=True)

# reservation db model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(255), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 


