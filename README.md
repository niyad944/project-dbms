#Mount n' Mist - Full Stack Hotel Booking Web Application
A complete, database-driven web application that simulates a real-world hotel booking system. Built with Python and Flask, this project allows users to sign up, log in, browse rooms, book a stay, and manage their booking history.

##Project Overview
Mount n' Mist is a demonstration of a full-stack web application. It provides a seamless user experience from authentication to booking confirmation. The backend is powered by Flask, handling all the business logic and database interactions, while the frontend uses clean HTML and CSS to create a modern, responsive user interface. The project manages rooms, user accounts, bookings, and billing through a relational SQLite database.

##Key Features
User Authentication: Secure user registration and login system with session management to handle user state.

Room Browsing: Users can view detailed pages for different room types available at the hotel.

Dynamic Booking System: A complete booking flow where users select dates, which creates a temporary "Pending" booking.

Payment Simulation: A dedicated payment confirmation page where a user can finalize their booking (updating the status to "Paid") or cancel it.

Booking History: A personalized section on the homepage where logged-in users can view their past and upcoming bookings, along with their payment status.

Secure Cancellation: Users can cancel their own bookings directly from their history page, with backend validation to ensure they cannot cancel bookings belonging to other users.

Relational Database: A well-structured SQLite database with cascading rules to ensure data integrity (e.g., canceling a booking automatically removes the associated bill).

##Tech Stack
Backend: Python 3, Flask

Database: SQLite 3

Frontend: HTML5, CSS3

Deployment: PythonAnywhere

##Running the Project Locally
To run this project on your own machine, follow these steps:

1. Clone the Repository:

git clone [https://github.com/your-username/mount-n-mist.git](https://github.com/your-username/mount-n-mist.git)
cd mount-n-mist

2. Create and Activate a Virtual Environment:
This isolates the project's dependencies.

###For Windows
python -m venv env
.\env\Scripts\activate

###For macOS/Linux
python3 -m venv env
source env/bin/activate

3. Install Dependencies:
The requirements.txt file contains all the necessary packages.

pip install -r requirements.txt

4. Set Up the Database (One-Time Task):
Run the setup script to create the hotel_management.db file and populate it with initial data.

python setup_database.py

5. Run the Flask Application:

flask run

The application will be available at http://127.0.0.1:5000.

##Deployment
This application is deployed and live on PythonAnywhere. The platform's persistent filesystem is ideal for hosting applications with an SQLite database, as it prevents data loss on server restarts.

Live URL: http://your-username.pythonanywhere.com

📁 Project Structure
/mount-n-mist
├── app.py                  # Main Flask application (routes and logic)
├── database.py             # All functions for database interaction
├── setup_database.py       # One-time script to create and populate the DB
├── requirements.txt        # Project dependencies
├── static/                 # CSS stylesheets, images
│   ├── css/
│   └── images/
└── templates/              # HTML templates
    ├── homepage.html
    ├── login.html
    ├── room.html
    └── ...
