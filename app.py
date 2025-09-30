from flask import Flask, request, render_template,redirect, url_for 
from database import signup as dbsignupfunction, login as dbloginfuncton


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
        redirect(url_for("login"))
    return render_template("signup.html")


if __name__=="__main__":
    app.run(debug=True)