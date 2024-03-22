from Hotel_Reservation import create_app
from Hotel_Reservation.models import Room
from Hotel_Reservation import db

# Flask application instance
app = create_app()

# database tables and add sample data within the application context
with app.app_context():
    # Create database tables
    db.create_all()
    # creating three rooms at first
    room_numbers = [101, 102, 103]
    existing_rooms = Room.query.filter(Room.room_number.in_(room_numbers)).all()
    for room_number in room_numbers:
        if not any(room.room_number == room_number for room in existing_rooms):
            sample_room = Room(room_number=room_number, amenities='Free Wi-Fi', capacity=2)
            db.session.add(sample_room)
    db.session.commit()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
