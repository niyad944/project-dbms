from flask import Flask, request, render_template,redirect, url_for 
from database import signup as dbsignupfunction, login as dbloginfuncton
import sqlite3

app=Flask(__name__)
@app.route("/",methods=["GET", "POST"])
def login():
    email=None
    password=None
    status=None
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        print(email)
        print(password)
        status=dbloginfuncton(email,password)
        if status==1:
            print("Login Successfull")
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

if __name__=="__main__":
    app.run(debug=True)