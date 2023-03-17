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
        return render_template("index.html")
    if request.method == "POST":
        return redirect("/")


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "GET":
        connect = connect_database(database)
        with connect:
            reviews = connect.execute("SELECT id, rating, name, review, time FROM reviews ORDER BY time DESC").fetchall()
            rating_average = connect.execute("SELECT ROUND(AVG(rating), 1) FROM reviews").fetchone()
        return render_template("reviews.html", reviews=reviews, rating_average=rating_average)
    if request.method == "POST":
        rating = request.form.get("rating")
        name = request.form.get("name")
        review = request.form.get("review")
        together = (rating, name, review)
        db = connect_database(database)
        if db.execute("INSERT INTO reviews(rating, name, review) VALUES(?, ?, ?)", together):
            db.commit()
            return render_template("/added.html")
        return redirect("/reviews")


@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        id = request.form.get("remove")
        connect = connect_database(database)
        connect.execute("DELETE FROM reviews WHERE id=?", [id])
        connect.commit()
        return redirect("/reviews")


@app.route("/game", methods=["GET", "POST"])
def game():
    global won
    won = False
    global size
    size = 4
    global spot
    global field
    # temp = {}
    # field = []
    # for i in range(size):
    #     for j in range(size ):
    #         temp['id'] = int(str(i+1) + str(j+1))
    #         print('clicked false')
    #         temp['clicked'] = False
    #         field.append(temp)
    #         temp = {}

    if request.method == "GET":
        spotX = random.randint(1, size)
        spotY = random.randint(1, size)
        spot = str(spotX) + str(spotY)
        print('spot', spot)
        return render_template("game.html", field=field, size=size)

    if request.method == "POST":
        print('new_game', request.form.get("new_game"))
        if request.form.get("new_game") == "new_game":
            spotX = random.randint(1, size)
            spotY = random.randint(1, size)
            spot = str(spotX) + str(spotY)
            print('spot', spot)

            temp = {}
            field = []
            for i in range(size):
                for j in range(size ):
                    temp['id'] = int(str(i+1) + str(j+1))
                    temp['clicked'] = False
                    field.append(temp)
                    temp = {}

            return render_template("game.html", field=field, size=size)

        while not won:
            # Get the ID of the sqaure that was clicked
            square = request.form.get("square")
            print('clicked square:', square)

            # Search in 'field' where is the square that was clicked and change it's boolean 'clicked' to True
            print(field)
            for i in range(len(field)):
                if int(square) == int(field[i]['id']):
                    field[i]['clicked'] = True
            print(field)
            # If the square that was clicked is the same where Garfield was hiding, the game is won
            if square == spot:
                print("Found Garfield!")
                won = True
                return render_template("won.html")
            if square != spot:
                print("wrong")
                no = "Wrong tile. Try again!"
                return render_template("game.html", field=field, size=size, no=no)

    return render_template("game.html")