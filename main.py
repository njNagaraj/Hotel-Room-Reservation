from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define the Room and Reservation models
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)
    reservations = db.relationship('Reservation', backref='room', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(255), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

# Create tables in the database
with app.app_context():
    db.create_all()

# Sample data for demonstration purposes
with app.app_context():
  room_number = 101
  existing_room = Room.query.filter_by(room_number=room_number).first()

  if not existing_room:
      sample_room = Room(room_number=room_number, amenities='Free Wi-Fi')
      db.session.add(sample_room)
      db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html', rooms=Room.query.all())

@app.route('/index0')
def index0():
  return render_template('index0.html')

@app.route('/room/<int:room_id>')
def room_details(room_id):
    room = Room.query.get(room_id)
    return render_template('room_details.html', room=room)

@app.route('/reservation/new', methods=['GET', 'POST'])
def reservation_form():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_id = request.form['room_id']

        reservation = Reservation(guest_name=guest_name,
                                  check_in_date=check_in_date,
                                  check_out_date=check_out_date,
                                  room_id=room_id)

        db.session.add(reservation)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('reservation_form.html', rooms=Room.query.all())

@app.route('/reservation/history')
def reservation_history():
    reservations = Reservation.query.all()
    return render_template('reservation_history.html', reservations=reservations)

@app.route('/admin')
def admin_panel():
    return render_template('admin_panel.html', rooms=Room.query.all(), reservations=Reservation.query.all())

@app.route('/search_rooms', methods=['GET', 'POST'])
def search_rooms():
    if request.method == 'POST':
        # Get search parameters from the form
        date_str = request.form['date']
        guests = int(request.form['guests'])

        # Convert the date string to a datetime object
        try:
            date = datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use MM/DD/YYYY.'})

        # Query available rooms based on the search parameters
        available_rooms = Room.query.filter(Room.id.notin_(
            db.session.query(Reservation.room_id).filter(
                (Reservation.check_in_date <= date) &
                (Reservation.check_out_date >= date)
            )
        )).all()

        return render_template('search_results.html', rooms=available_rooms, search_date=date, guests=guests)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
