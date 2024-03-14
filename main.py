from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for flashing messages
db = SQLAlchemy(app)
bcrypt = Bcrypt()

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

class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)


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
@app.route('/', methods=['GET', 'POST'])
def main_index():
    return render_template('main_index.html')

@app.route('/index')
def index():
    return render_template('index.html', rooms=Room.query.all())

@app.route('/room/<int:room_id>')
def room_details(room_id):
    room = Room.query.get(room_id)
    return render_template('room_details.html', room=room)

@app.route('/reservation/new', methods=['GET', 'POST'])
def reservation_form():
    if request.method == 'POST':
        if 'logged_in_user' not in session:
            flash("Please log in to make a reservation.", "error")
            return redirect(url_for('customer_login'))

        guest_name = request.form['guest_name']
        check_in_date_str = request.form['check_in_date']
        check_out_date_str = request.form['check_out_date']
        room_id = request.form['room_id']

        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

        reservation = Reservation(guest_name=guest_name,
                                  check_in_date=check_in_date,
                                  check_out_date=check_out_date,
                                  room_id=room_id)

        db.session.add(reservation)
        db.session.commit()

        flash("Reservation made successfully!", "success")
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
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        guests = int(request.form['guests'])

        try:
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use MM/DD/YYYY.'})

        if end_date <= start_date:
            return jsonify({'error': 'End date must be after the start date.'})

        available_rooms = Room.query.filter(Room.id.notin_(
            db.session.query(Reservation.room_id).filter(
                (Reservation.check_in_date <= end_date) &
                (Reservation.check_out_date >= start_date)
            )
        )).all()

        return render_template('search_results.html', rooms=available_rooms, start_date=start_date, end_date=end_date, guests=guests)

    elif request.method == 'GET':
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        guests = int(request.args.get('guests'))

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        booked_room_ids = [reservation.room_id for reservation in Reservation.query.filter(Reservation.check_in_date <= end_date, Reservation.check_out_date >= start_date).all()]
        available_rooms = Room.query.filter(Room.id.notin_(booked_room_ids)).all()

        return render_template('search_results.html', rooms=available_rooms)

    return redirect(url_for('index'))

@app.route('/admin/add_room', methods=['POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        amenities = request.form['amenities']

        existing_room = Room.query.filter_by(room_number=room_number).first()
        if existing_room:
            flash('Room number already exists.', 'danger')
            return redirect(url_for('admin_panel'))

        new_room = Room(room_number=room_number, amenities=amenities)
        db.session.add(new_room)
        db.session.commit()

        flash('Room added successfully!', 'success')
        return redirect(url_for('admin_panel'))


@app.route('/admin/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)

    if request.method == 'POST':
        room.room_number = request.form['room_number']
        room.amenities = request.form['amenities']

        db.session.commit()

        flash('Room updated successfully!', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('edit_room.html', room=room)

@app.route('/admin/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()

    flash('Room deleted successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation canceled successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/new-customer', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_customer = Customer.query.filter_by(username=username).first()
        if existing_customer:
            flash("An account with this username already exists. Please choose a different username.", 'error')
            return redirect(url_for('new_customer'))

        if password != confirm_password:
            flash("Password and Confirm Password do not match. Please try again.", 'danger')
            return redirect(url_for('new_customer'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_customer = Customer(username=username, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()

        flash(f"Account created successfully for {username}. You can now log in.", 'success')
        return redirect(url_for('customer_login'))

    return render_template('new_customer.html')

@app.route('/customer-login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        customer = Customer.query.filter_by(username=username).first()

        if customer:
            hashed_password = customer.password
            if bcrypt.check_password_hash(hashed_password, password):
                session['logged_in_user'] = username
                flash("Your login was successful!", "success")

                # Retrieve the previous page URL from the session
                prev_page = session.get('prev_page')
                if prev_page:
                    session.pop('prev_page')  # Clear the previous page URL from the session
                    return redirect(prev_page)
                else:
                    # If no previous page is stored, redirect to a default page
                    return redirect(url_for('index'))

            else:
                flash("Incorrect password. Please try again.", 'error')
        else:
            flash("Username not found. Please create an account first.", 'error')

    # If the request method is GET or login fails, redirect back to the login page
    # Store the previous page URL in the session before redirecting
    session['prev_page'] = request.referrer
    return render_template('customer_login.html')

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_panel'))
        else:
            flash("Incorrect admin username or password. Please try again.", 'error')

    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
