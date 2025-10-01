from flask import Flask, request, render_template,redirect, url_for,session
from database import signup as dbsignupfunction, login as dbloginfuncton, book_room 
import sqlite3



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
            session['user_id'] = user['GuestID']
            session['user_name'] = user['Name']
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
    return render_template("homepage.html")

@app.route("/room/<int:room_id>")
def room_page(room_id):
    conn = sqlite3.connect("hospital_management.db")
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
    
    # Get the logged-in guest's ID from the session
    guest_id = session['user_id']
    
    message = book_room(guest_id, room_type_id, check_in, check_out)
    
    # Flash the result message to the user
    print(message)
    return redirect(url_for('room_page', room_id=room_type_id))



if __name__=="__main__":
    app.run(debug=True)