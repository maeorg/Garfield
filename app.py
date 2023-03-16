from flask import Flask, render_template, request
import random
import sqlite3


app = Flask(__name__)
# export FLASK_DEBUG=1


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        db = sqlite3.connect("database.db")
        reviews = db.execute("SELECT * FROM reviews")
        print(reviews)
        return render_template("index.html", reviews=reviews)
    if request.method == "POST":
        #if not request.form.get("name"):

        #name = request.form.get("name")
        
        #review = request.form.get("review")
        return render_template("index.html")


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