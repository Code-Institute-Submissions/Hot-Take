import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html", page_title="Welcome To Hot Take")


@app.route("/albums")
def albums():
    albums = mongo.db.album_data.find()
    return render_template("albums.html", albums=albums, page_title="Albums")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username exists in database
        existing_username_check = mongo.db.users.find_one(
            {"username": request.form.get("inputusername4").lower()})

        # check if email exists in database
        existing_email_check = mongo.db.users.find_one(
            {"email": request.form.get("inputEmail3").lower()})

        if existing_email_check:
            flash("This Email is already in use, please use a diffrent email.")
            return redirect(url_for("register"))

        if existing_username_check:
            flash("This Username already exists, try something different.")
            return redirect(url_for("register"))

        register = {
            "fist_name": request.form.get("inputFirstName1"),
            "last_name": request.form.get("inputLastName2"),
            "email": request.form.get("inputEmail3"),
            "username": request.form.get("inputusername4").lower(),
            "password": generate_password_hash(
                request.form.get("inputPassword5"))
        }
        mongo.db.users.insert_one(register)

        # This will enter the new users info into a 'session' cookie
        session["user"] = request.form.get("inputusername4").lower()
        flash("Registration Successfully Completed!")
    return render_template("register.html", page_title="Register")


@app.route("/profile")
def profile():
    return render_template("profile.html", page_title="Profile")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/sign_in")
def sign_in():
    return render_template("sign-in.html", page_title="Sign in")


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
