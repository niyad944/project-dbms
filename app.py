from flask import Flask, request, render_template


app=Flask(__name__)
@app.route("/",methods=["GET", "POST"])
def login():
    email=None
    password=None
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        print(email)
        print(password)
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
        print(username)
        print(email)
        print(password)
        print(phone)
    return render_template("signup.html")


if __name__=="__main__":
    app.run(debug=True)