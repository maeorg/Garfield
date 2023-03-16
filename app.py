from flask import Flask, render_template, request, redirect
import random
import sqlite3


app = Flask(__name__)
# export FLASK_DEBUG=1

# Database file
database = "database.db"


# Connect to the database
def connect_database(database):
    connect = None
    try:
        connect = sqlite3.connect(database)
    except Error as e:
        print(e)
    return connect


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        connect = connect_database(database)
        with connect:
            reviews = connect.execute("SELECT * FROM reviews").fetchall()
            rating_average = connect.execute("SELECT ROUND(AVG(rating), 1) FROM reviews").fetchone()
            print(rating_average)
        return render_template("index.html", reviews=reviews, rating_average=rating_average)
    if request.method == "POST":
        rating = request.form.get("rating")
        name = request.form.get("name")
        review = request.form.get("review")
        together = (rating, name, review)
        db = connect_database(database)
        db.execute("INSERT INTO reviews(rating, name, review) VALUES(?, ?, ?)", together)
        db.commit()
        return redirect("/")


@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "GET":
        spotX = random.randint(1, 4)
        spotY = random.randint(1, 4)
        global spot
        spot = "b" + str(spotX) + str(spotY)
        print(spot)
        return render_template("game.html")
    if request.method == "POST":
        print("Form!")
        print(spot)
        if request.form.get(spot) == "b":
            print("Found Garfield!")
            return render_template("won.html")
        for i in range(1, 5):
            for j in range(1, 5):
                pushed = "b" + str(i) + str(j)
                if request.form.get(pushed) == "b":
                    print("wrong")
                    no = "Wrong tile. Try again!"
                    return render_template("game.html", no=no)

        return render_template("game.html")