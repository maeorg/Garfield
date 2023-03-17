function ifEmpty() {
    var rating = document.forms["review"]["rating"].value;
    var name = document.forms["review"]["name"].value;
    var review = document.forms["review"]["review"].value;
    if (rating == null || rating == "" || rating < 1 || rating > 5 || isNaN(rating)) {
        alert("Rating has to be a number from 1 to 5.");
        return false;
    }
    if (name == null || name == "") {
        alert("Please insert name.");
        return false;
    }
    if (review == null || review == "") {
        alert("Please insert review.");
        return false;
    }
}

function sizeCheck() {
    var size = document.forms["new_game"]["size"].value;
    if (size == null || size <= 0 || isNaN(size)) {
        alert("Field size has to be a positive number.");
        return false;
    }
}

function fieldCheck() {
    var name = document.forms["enter_score"]["name"].value;
    if (name == null || name == "" || !name.match(/^[A-Za-z0-9]*$/)) {
        alert("Enter valid name");
        return false;
    }
}