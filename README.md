# Hotel Reservation System

## Overview
The goal of this project is to create a simple yet efficient hotel reservation system that enables customers to search for available rooms and make reservations hassle-free.

Upon the initial launch of the application, only one demo room will be created with room number 101 with default image. Additional rooms can be added by logging in as an admin using the username "admin" and password "admin". (if further rooms are created all rooms will have same image for now)

The code is perfectly organised with template inheritance, Packages and Blueprints.

Handled all the erorr cases and a fully functional website working situations

## Tools Used

- Flask
- SQL Alchemy for database interaction
- SQLite for database management
- Flask Login for authentication and more small packages for other functionalities.

## Functionality

### Customer

- **Search for Available Rooms**: Customers can search for available rooms based on their preferred date range and the number of guests.

- **View Room Details**: Customers can view detailed information about each room, including amenities, before making a reservation.

- **Make a Reservation**: Customers can make reservations by selecting a room and entering their personal details.

- **View Reservation History**: Customers can view their reservation history and cancel a reservation if necessary. Logging in is required for booking a reservation, but any customer can view available rooms. 

- **Filter by Dates**: Customers can apply filters based on dates to see available rooms. Booked rooms for specific dates will be removed from the available rooms list.

### Admin

- **Add, Edit, and Delete Rooms**: Admins have the ability to add, edit, and delete rooms from the system.

- **View Reservations**: Admins can view a list of reservations and cancel reservations if needed. 

- **Admin Login**: Admins can log in with their credentials (username: admin, password: admin) to access the admin functionalities.

## Running the Application

To run the application from the command line:

Install Git and Python before proceed git-https://git-scm.com/downloads and python-https://www.python.org/downloads/

1. Clone the repository:
    ```
    git clone https://github.com/njNagaraj/Hotel-room-reservation.git
    ```

2. Navigate to the project directory:
    ```
    cd Hotel-room-reservation
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run the application:
    ```
    flask --app main run
    ```

if any error happens while cloning the repo just download the zip and extract and go to the project directory and execute the above point 3 and 4 comments
