from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .forms import ReservationForm
from Hotel_Reservation.models import Room, Reservation
from Hotel_Reservation import db

# creating a blueprint for rooms
rooms = Blueprint('rooms', __name__)

# customer index page route
@rooms.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html', rooms=Room.query.all(), title="Rooms")

# Room details route
@rooms.route('/room/<int:room_id>')
def room_details(room_id):
    form = ReservationForm()
    room = Room.query.get(room_id)
    return render_template('rooms/room_details.html', room=room, form=form, title="Room Details")

# Search rooms route
@rooms.route('/search_rooms', methods=['GET', 'POST'])
def search_rooms():
    if request.method == 'POST':
        # Retrieve form data from POST request
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        guests = int(request.form['guests'])

        # Convert date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use MM/DD/YYYY.'})

        # Check if end date is after start date
        if end_date <= start_date:
            return jsonify({'error': 'End date must be after the start date.'})

        # Query available rooms based on date range and guest count
        available_rooms = Room.query.filter(Room.id.notin_(
            db.session.query(Reservation.room_id).filter(
                (Reservation.check_in_date <= end_date) &
                (Reservation.check_out_date >= start_date)
            )
        )).filter(Room.capacity >= guests)  # Filter rooms by capacity
        available_rooms = available_rooms.all()

        return render_template('rooms/search_results.html', rooms=available_rooms, start_date=start_date, end_date=end_date, guests=guests, title="Room Details")

    # Handle GET requests for room search
    elif request.method == 'GET':
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        guests = int(request.args.get('guests'))

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Query booked room IDs for the given date range
        booked_room_ids = [reservation.room_id for reservation in Reservation.query.filter(Reservation.check_in_date <= end_date, Reservation.check_out_date >= start_date).all()]

        # Query available rooms based on booked room IDs and guest count
        available_rooms = Room.query.filter(Room.id.notin_(booked_room_ids)).filter(Room.capacity >= guests)
        available_rooms = available_rooms.all()

        return render_template('rooms/search_results.html', rooms=available_rooms, title="Room Details")

    return redirect(url_for('rooms.index'))
