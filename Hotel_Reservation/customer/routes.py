from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import SignUpForm, LoginForm
from Hotel_Reservation.models import Room, Reservation, Customer
from datetime import datetime
from Hotel_Reservation import bcrypt, db

customer = Blueprint('customer', __name__)

# New customer signup route
@customer.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('rooms.index'))
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
      
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('customer.sign_up'))
        # dehashing password and cheking password is correct
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_customer = Customer(username=username, email=email, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('customer.login'))
    return render_template('customer/sign_up.html', form=form, title="Sign Up")

# Customer login route
@customer.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('rooms.index'))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        customer = Customer.query.filter_by(username=username).first()
        if customer:
              hashed_password = customer.password
              if bcrypt.check_password_hash(hashed_password, password):
                  login_user(customer)
                  next_page = request.args.get('next')
                  flash("Your login was successful!", "success")
                  return redirect(next_page) if next_page else redirect(url_for('rooms.index'))
              else:
                  flash("Incorrect password. Please try again.", 'danger')
        else:
              flash("Username not found. Please create an account first.", 'danger')
              return redirect(url_for('customer.sign_up'))

    return render_template('customer/login.html', title="Login", form=form)

@customer.route('/reservation_form', methods=['GET', 'POST'])
@login_required
def reservation_form():
    if not current_user.is_authenticated:
        return redirect(url_for('customer.login'))
      
    if request.method == 'POST':
        # Getting form data
        guest_name = request.form['guest_name']
        check_in_date_str = request.form['check_in_date']
        check_out_date_str = request.form['check_out_date']
        room_id = request.form['room_id']

        room = Room.query.get(room_id)
        # Parse dates
        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

        # Check if end date is greater than start date
        if check_out_date <= check_in_date:
            flash("End date must be greater than start date.", "danger")
            return redirect(url_for('rooms.room_details', room_id=room_id))

        # Check if the room is available for the provided dates
        if room:
            reservations = Reservation.query.filter_by(room_id=room_id).all()
            for reservation in reservations:
                if (check_in_date >= reservation.check_in_date and check_in_date <= reservation.check_out_date) or \
                   (check_out_date >= reservation.check_in_date and check_out_date <= reservation.check_out_date):
                    flash("This room is already booked for the selected dates.", "danger")
                    return redirect(url_for('rooms.room_details', room_id=room_id))
        else:
            flash("Room not found.", "danger")
            return redirect(url_for('rooms.room_details', room_id=room_id ))

        # Make the reservation
        customer = Customer.query.filter_by(username=current_user.username).first()
        if customer:
            reservation = Reservation(guest_name=guest_name, check_in_date=check_in_date, check_out_date=check_out_date, room_id=room_id, customer_id=customer.id)
            db.session.add(reservation)
            db.session.commit()
            flash("Reservation made successfully!", "success")
            return redirect(url_for('customer.view_reservation', reservation_id=reservation.id))
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('customer.login'))

    return render_template('rooms.room_details', room=Room.query.all())

@customer.route('/reservation/<int:reservation_id>')
@login_required
def view_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    return render_template('customer/view_reservation.html', reservation=reservation, title="Reservation Details")

# Reservation history route 
@customer.route('/reservation/history')
@login_required
def reservation_history():
    if current_user.is_authenticated:
        customer = Customer.query.filter_by(username=current_user.username).first()
        if customer:
            reservations = Reservation.query.filter_by(customer_id=customer.id).all()
            return render_template('customer/reservation_history.html', reservations=reservations, title="Reservation History")
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('customer.login', next=request.url)) 
    else:
        flash('Please log in to view your reservation history.', 'danger')
        return redirect(url_for('customer.login', next=request.url)) 

# Cancel reservation route
@customer.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation canceled successfully!', 'success')
    return redirect(url_for('customer.reservation_history'))
  
# User logout route
@customer.route('/user_logout')
def user_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main_page.main'))