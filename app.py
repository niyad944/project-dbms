from flask import Flask, request, render_template,redirect, url_for,session,flash
from database import signup as dbsignupfunction, login as dbloginfuncton, book_room, update_bill_to_paid, get_pending_booking_details,cancel_pending_booking,get_booking_history_for_guest
import sqlite3
import os

DATA_DIR = os.environ.get('ONRENDER_DISK_PATH', '.')
DB_FILE = os.path.join(DATA_DIR, "DB_FILE.db")

app=Flask(__name__)
app.secret_key = '0f1e8a9d7c6b5a3e4f2a1b9c8d7e6f5a' 
@app.route("/",methods=["GET", "POST"])
def login():
    email=None
    password=None
    status=None
    user=None
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        print(email)
        print(password)
        user,status=dbloginfuncton(email,password)
        if status==1:
            print("Login Successfull")
            session['useremail'] = email
            return redirect(url_for("homepage"))
        else:
            print("Invalid Credentials")
    return render_template("login.html")

@app.route("/signup",methods=["GET", "POST"])
def signup():
    username=None
    email=None
    password=None
    phone=None
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        phone=request.form.get("phone")
        dbsignupfunction(username,email,password,phone)
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/homepage")
def homepage():
    useremail=session.get("useremail")

    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Guests WHERE Email = ?", (useremail,))
    
    # fetchone() gets the first result
    username = cursor.fetchone()
    for i in username:
        username=i

    cursor.execute("SELECT GuestID FROM Guests WHERE Email = ?", (useremail,))
    guestid = cursor.fetchone()
    for i in guestid:
        guestid=i
    booking_history = get_booking_history_for_guest(guestid)
    
    return render_template("homepage.html", username=username, bookings=booking_history)
    
    conn.close()
    return render_template("homepage.html",username=username)

@app.route("/room/<int:room_id>")
def room_page(room_id):
    conn = sqlite3.connect("DB_FILE.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RoomTypes WHERE RoomTypeID=?", (room_id,))
    room = cursor.fetchone()
    if not room:
        return "Room not found", 404
    return render_template("room.html", room=room)


@app.route('/book', methods=['POST'])
def book():
    room_type_id = request.form.get('room_type_id')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')

    print("room_type_id: ",room_type_id)
    print("check_in: ",check_in)
    print("check_out:",check_out)
    
    guest_id = session['user_id']
    message,billing_id  = book_room(guest_id, room_type_id, check_in, check_out)
    print(message)
    if billing_id!=-1:
        return redirect(url_for('payment_page', billing_id=billing_id))
    else:
        return redirect(url_for('room_page', room_id=room_type_id))

    return redirect(url_for('room_page', room_id=room_type_id))

@app.route('/payment/<int:billing_id>')
def payment_page(billing_id):
    details = get_pending_booking_details(billing_id)
    
    if not details:
        print("Booking not found or already processed.")
        return redirect(url_for('homepage'))
        
    return render_template('payment.html', details=details)


@app.route('/process_payment', methods=['POST'])
def process_payment():
    billing_id = request.form.get('billing_id')
    message = update_bill_to_paid(billing_id)
    print(message)
    return redirect(url_for('homepage'))


@app.route('/cancel_payment', methods=['POST'])
def cancel_payment():
    booking_id = request.form.get('booking_id')
    message = cancel_pending_booking(booking_id)

    print(message)
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)


'''if __name__=="__main__":
    app.run(debug=True)'''