# Hotel reservation system

# Overview
The goal of this project is to create a hotel reservation system that allows customers to search for available rooms and make reservations.

# Functionality
Customer

As a customer, I can search for available rooms based on the date range and number of guests.

As a customer, I can view room details and amenities before making a reservation.

As a customer, I can make a reservation by selecting a room and entering my personal details.

As a customer, I can view my reservation history and cancel a reservation if needed.


(The customer able book rooms only if they create account and loggged in but any customer can see the available rooms login is only needed for booking reservation

Each user can view their reservation after done and able to cancel reservation after booking only and also able to see the reservation history

THe customer can apply filter by dates and get the available rooms 

if one room is booked then it will not be booked by anyone after applyimg filter the bokked rooms with particular dates will be removed)


Admin

As an admin, I can add, edit, and delete rooms.

As an admin, I can view a list of reservations and cancel reservations if needed.


(the admin is able to login with his credential hear username = admin and password = admin and able to see edit add room details and ale to cancel the customer registration)

# TOOLS USED

Flask

SQL Alchemy

sqlite


# To run in cmd

(make sure git is installed)

git clone https://github.com/njNagaraj/Hotel-room-reservation.git

then move to the project directory inside Hotel-room-reservation 

pip install -r requirements.txt

then

flask --app main run


