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


# find game and show its related comments
@app.route("/albums/<album_id>", methods=["GET", "POST"])
def album(game_id):
    album = mongo.db.albums.find_one({"_id": ObjectId(game_id)})
    reviews = list(mongo.db.review.find({"game_id": ObjectId(game_id)}))
    return render_template("album.html", game=game, comments=comments)


@app.route("/add_album", methods=["GET", "POST"])
def add_album():
    # prevent brute force
    if session.get("user"):
        if request.method == "POST":
            stream_link = (
                "https://open.spotify.com/search/" + request.form.get(
                    "inputAlbumTitle1"))
            # get album info from the form
            album = {
                "title": request.form.get("inputAlbumTitle1"),
                "artist": request.form.get(""),
                "relaste_date": request.form.get(""),
                "cover_art": request.form.get(""),
                "genre": request.form.get("inputGenre5"),
                "stream_link": stream_link
            }
            # write new album data into database
            mongo.db.insert_one(album)
            flash("Album Succesfully Added")
            return redirect(url_for("albuums"))
        genres = mongo.db.genres.find().sort("genre", 1)
        return render_template("add-album.html", genres=genres)
    flash("You need to sign in to add a new album!")
    return redirect(url_for("sign_in"))


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
            "email": request.form.get("inputEmail3").lower(),
            "username": request.form.get("inputusername4").lower(),
            "password": generate_password_hash(
                request.form.get("inputPassword5"))
        }
        mongo.db.users.insert_one(register)

        # This will enter the new users info into a 'session' cookie
        session["user"] = request.form.get("inputusername4").lower()
        flash("Registration Successfully Completed!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html", page_title="Register")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template(
            "profile.html", username=username, page_title="Profile")

    return redirect(url_for("sign_in"))


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # see if the user exists by checking the email exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("inputusername4").lower()})

        if existing_user:
            # Check the hashed password matchesthe inputted pass.
            if check_password_hash(existing_user["password"], request.form.get(
                    "inputPassword5")):
                session["user"] = request.form.get("inputusername4").lower()
                flash("Welcome back {}! What you been listning to?".format(
                    request.form.get(
                        "inputusername4")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # Passwords don't match!
                flash("Incorect Username/Password")
                return redirect(url_for('sign_in'))

        else:
            # username isnt registered on database
            flash("Incorect Username/Password")
            return redirect(url_for('sign_in'))

    return render_template("sign-in.html", page_title="Sign in")


@app.route("/logout")
def logout():
    # removes session cookie data
    flash("Log out Completed")
    session.pop("user")
    return redirect(url_for("sign_in"))


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
