from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login.utils import login_user, current_user, logout_user
from .forms import AddRoomForm, EditRoomForm, AdminLoginForm
from Hotel_Reservation.models import Room, Reservation
from Hotel_Reservation import db

admin = Blueprint('admin', __name__)

# Admin login route
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

@admin.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            flash('You have been logged in.', 'success')
            login_user(current_user)
            return redirect(url_for('admin.admin_panel'))
        else:
            print("Incorrect credentials")
            flash('Incorrect username or password.', 'danger')
    return render_template('admin/admin_login.html', title="Admin Login", form=form)

# admin index panel
@admin.route('/admin_panel')
def admin_panel():
    form = AddRoomForm()
    return render_template('rooms/view_rooms.html', form=form, rooms=Room.query.all(), reservations=Reservation.query.all(), title="Admin Panel")

# add room route
@admin.route('/admin/add_room', methods=['GET', 'POST'])
def add_room():
    form = AddRoomForm()
    if form.validate_on_submit():
        room_number = form.room_number.data
        amenities = form.amenities.data
        capacity = form.capacity.data
        existing_room = Room.query.filter_by(room_number=room_number).first()
        if existing_room:
            flash('Room number already exists.', 'danger')
            return redirect(url_for('admin.admin_panel'))
        new_room = Room(room_number=room_number, amenities=amenities, capacity=capacity)
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin/add_room.html', form=form)

# Edit room route
@admin.route('/admin/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    form = EditRoomForm(obj=room)
    if form.validate_on_submit():
        form.populate_obj(room)
        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('admin.admin_panel'))
    return render_template('rooms/edit_room.html', form=form, room=room, title="Edit Room")

# Delete room route
@admin.route('/admin/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('admin.admin_panel'))

#admin view rooms
@admin.route('/admin/view_rooms')
def view_rooms():
    rooms = Room.query.all()
    return render_template('rooms/view_rooms.html', rooms=rooms, title="View Rooms")

#all reservations
@admin.route('/admin/all_reservations')
def all_reservations():
    reservations = Reservation.query.all()
    return render_template('admin/all_reservations.html', reservations=reservations, title="All Reservation")

# admin cancel reservation
@admin.route('/ressdfdservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation canceled successfully!', 'success')
    return redirect(url_for('admin.all_reservations'))

# admin logout route
@admin.route('/admin_logout', methods=['POST', 'GET'])
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main_page.main'))




