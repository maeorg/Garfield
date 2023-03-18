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

# The homepage/index page. Not much happening here
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        return redirect("/")


# This is where the logic for handling reviews is
@app.route("/reviews", methods=["GET", "POST"])
def reviews():   
    if request.method == "GET":

        # Connects to the database, executes SQL to select all reviews and puts them in a list
        connect = connect_database(database)
        with connect:
            reviews = connect.execute("SELECT id, rating, name, review, time FROM reviews ORDER BY time DESC").fetchall()

            # Gets the average rating score from the database
            rating_average = connect.execute("SELECT ROUND(AVG(rating), 1) FROM reviews").fetchone()

        # Renders the reviews html page along with the reviews list from database and average rating score
        return render_template("reviews.html", reviews=reviews, rating_average=rating_average)

    if request.method == "POST":

        # Gets inputs from the form and puts them together into one list variable
        rating = request.form.get("rating")
        name = request.form.get("name")
        review = request.form.get("review")
        together = (rating, name, review)

        # Connects to database and inserts into it the formentioned list of data (rating, name, review)
        db = connect_database(database)
        if db.execute("INSERT INTO reviews(rating, name, review) VALUES(?, ?, ?)", together):
            db.commit()

            # Sets the variable 'added' to True to indicate that the database insertion was a success
            added = True
            
            # Gets all reviews from database along with average rating score
            with db:
                reviews = db.execute("SELECT id, rating, name, review, time FROM reviews ORDER BY time DESC").fetchall()
                rating_average = db.execute("SELECT ROUND(AVG(rating), 1) FROM reviews").fetchone()

            # Renders the reviews html again along with the list of all reviews, average rating score and the boolen 'added' to indicate successful add
            return render_template("reviews.html", reviews=reviews, rating_average=rating_average, added=added)

        return redirect("/reviews")


# Removes reviews from database
@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":

        # Gets the id of the review that is to be removed from the form
        id = request.form.get("remove")

        #Connects to database and executes delete SQL and commits it to the database
        connect = connect_database(database)
        connect.execute("DELETE FROM reviews WHERE id=?", [id])
        connect.commit()

        # Returns back to the reviews page
        return redirect("/reviews")


# This is where most of the game logic is
@app.route("/game", methods=["GET", "POST"])
def game():
    # Sets the global variables that are needed to access from different functions/methods
    global won
    won = False
    global size
    global spot
    global field
    global count

    if request.method == "GET":
        return render_template("game.html")

    if request.method == "POST":

        # Checks if the new_game button was clicked. If yes then continue
        if request.form.get("new_game") == "new_game":

            # Gets the field size from form
            size = int(request.form.get("size"))

            # Randomly calculates the spot where Garfield is hiding, using x and y cordinates, with the parameters of the field size
            spotX = random.randint(1, size)
            spotY = random.randint(1, size)
            spot = str(spotX) + str(spotY)

            # Prints out to terminal the location of Garfield, for testing and debugging purposes
            print('spot', spot)

            # Sets a temporary variable to empty dictionary
            temp = {}

            # Sets the field variable to empty array list
            field = []

            # Iterates over each square of the field to create the whole field
            for i in range(size):
                for j in range(size ):

                    # Sets correct id to each square (row number + column number)
                    temp['id'] = int(str(i+1) + str(j+1))

                    # Sets the 'clicked' variable of each square to False
                    temp['clicked'] = False

                    # Adds the newly created square to the field
                    field.append(temp)

                    # Resets the temporary variable to empty
                    temp = {}

            # Renders the game html page along with the field data and field size
            return render_template("game.html", field=field, size=size)

        while not won:
            # Gets the ID of the sqaure that was clicked
            square = request.form.get("square")

            # Searches in 'field' where is the square that was clicked and changes it's boolean 'clicked' to True
            for i in range(len(field)):
                if int(square) == int(field[i]['id']):
                    field[i]['clicked'] = True
                    
            # If the square that was clicked is the same where Garfield was hiding, sets the variable 'won' to True to indicate the game was won
            if square == spot:
                won = True
                
                # Counts how many clicks it takes to find Garfield
                count = 0
                for i in range(len(field)):
                    if field[i]['clicked'] == True:
                        count += 1

                # Renders the game html page again along with the data about the game being won and the count of how many tries it took to find Garfield
                return render_template("game.html", won=won, count=count)

            # Checks in what direction is the square that was clikced from Garfields spot and gives directions accordingly
            direction = ''
            if square != spot:
                if spot[0] == square[0]:
                    if spot[1] < square[1]:
                        direction = "to the left"
                    if spot[1] > square[1]:
                        direction = "to the right"
                elif spot[1] == square[1]:
                    if spot[0] < square[0]:
                        direction = "up"
                    if spot[0] > square[0]:
                        direction = "down"
                elif spot[1] != square[1]:
                    if spot[1] < square[1]:
                        direction = "to the left"
                    if spot[1] > square[1]:
                        direction = "to the right"
                elif spot[1] != square[1]:
                    if spot[0] < square[0]:
                        direction = "up"
                    if spot[0] > square[0]:
                        direction = "down"

                # Sets variable 'no' to include the message about clicking the wrong square and also with directions to Garfield
                no = "Wrong tile. Try again! Garfield is more " + direction

                # Renders the game html page with the given field and field size and a response for clicking the wrong square
                return render_template("game.html", field=field, size=size, no=no)

    # Renders the game html page again
    return render_template("game.html")


@app.route("/highscores", methods=["GET", "POST"])
def highscores():
    if request.method == "GET":

        # Connects to the database
        db = connect_database(database)

        # With the database conenction open, executes a SQL command to select top 10 highscores from the highscores table
        with db:
            highscores = db.execute("SELECT * FROM highscores ORDER BY score ASC LIMIT 10").fetchall()

        # Renders the highscores html page with the data that it got from the previous SQL query to displays the table of highscores
        return render_template("highscores.html", highscores=highscores)

    if request.method == "POST":

        # Connects to the database
        db = connect_database(database)

        # Gets name from the game form to insert into highscores table
        name = request.form.get("name")

        # Buts together the name it previously got and the count of how many tries it took to find Garfield
        together = (name, count)

        # Saves highscore to database
        if db.execute("INSERT INTO highscores(name, score) VALUES(?, ?)", together):
            db.commit()

        # Goes to the highscores page to view the table of highscores
        return redirect("/highscores")