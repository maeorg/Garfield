from flask import Flask, render_template, request
import random

app = Flask(__name__)
app.run(debug=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        print("Form submitted!")
        color = request.form.get("color")
        return render_template("game.html", color=color)


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