from Hotel_Reservation import create_app
from Hotel_Reservation.models import Room
from Hotel_Reservation import db

# Flask application instance
app = create_app()

# database tables and add sample data within the application context
with app.app_context():
    # Create database tables
    db.create_all()

    # Check if sample room exists, if not, add it to the database
    room_number = 101
    existing_room = Room.query.filter_by(room_number=room_number).first()

    if not existing_room:
        sample_room = Room(room_number=room_number, amenities='Free Wi-Fi', capacity=2)
        db.session.add(sample_room)
        db.session.commit()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
