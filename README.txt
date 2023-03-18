# The game of Garfield
#### Video Demo:  <URL HERE>
#### Description:

This is the CS50 final project by Katrina Mäeorg. 2023 Estonia

My project is a webpage that contains a fun game that I made about finding Garfield. It includes the game, highscores and also reviews. It's a fullstack built from scratch project. It uses HMTL, CSS, Bootstrap, Flask, Jinja, Python, Javascript, SQLite - all the fun things we learned in our lectures and problem sets in CS50.

Here is a breakdown of all the files for the project:

HTML:
- layout.html
Here is where the magic happens. This is the main layout page that is extended in all the other html pages. Here lays the menu navigation part and also the footer part. I used Bootstrap to beautify the navigation menu. It also includes the reference to my Javascript file that holds the javascript functions.

- index.html
This is the main index page. It displays a welcome message and a big picture of Garfield.

- game.html
Here is where the game happens. You can choose the size of the game field and when clicking "New game" it will draw you the field with the chosen size. The objective of the game is to find Garfield that is hidden in the game field. Then you have to start clicking on the squares. With each click there are directions shown under the game field to guide you in the direction of Garfield. If you find him, a message is displayed that you won and information about how many tries it took you. Also a option is displayed to enter your score into the highscores table.

- highscores.html
Here is where the top 10 highscores are displayed. It gets information from app.py where the SQL query to the database is run to get the results to display.

- reviews.html
Here is where the reviews are displayed and also includes an option to add your own review. At the very top it displays the average rating score of the game, which is calculated based on all the ratings that are saved into the database. The review adding form has javascript checks written on it to prevent sending empty fields data into database with SQL. After successfuly adding a review a message is displayed with a cool picture of Garfield. Under the review adding form there are all the reviews displayed. I used bootstrap beautification options to make it look a bit nicer. What it does it loops over all the reviews (the query result it got from SQL database) and draws each review in a different nice card box. I also added a button there to be able to remove a review (mostly because it got very annoying to remove them manualy from the database when I was overflowing it with testing data while development).

Python:
- app.py
Here is where the Python magic happens. The file itself is fairly commented so I hope who is interested will check it out and find everything they need there as far as explanations about the pages and game logic etc. I really like the Python part the best, but it was also fun to do the HTML etc frontend part and get it all to work together. 

SQLite:
- database.db
This is where I store the necessary data. It has one table to store the highscores and another table to store the reviews. It is accessed from my Python script via SQL commands.

- sql.txt
Here I put my SQL table creation commands, just in case, if I ever need to delete the tables etc, it makes further improvement easier for me.

Javascript:
- myscripts.js
Here are three functions. One of them I use to check that into the game field size input box is inserted only positive integers. Everything else gets an alert message. The other function is for the review adding form, where I check that all the fields are filled and also that the rating would be a positive number between 1 and 5. The third function is to check that the name box is filled when entering the score into the highscore table after winning the game.

CSS:
- styles.css
Here's the CSS data. Nothing too crazy, just a couple of tweaks to the design and layout.

Images:
- Garfield_hello.jpg
The image of Garfield that is displayed at the index welcome page.

- garfield_thumbs_up.jpg
The image of Garfield that is displayed after successfuly entering a review.

- garfield_small.jpg
The image of Garfield that is displayed on every review card, to make it look more fun and nice.

- garfield.jpg
The image of Garfield that is displayed after winning the game.

