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
