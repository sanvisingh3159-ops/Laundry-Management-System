<<<<<<< HEAD
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "preview-key"      # needed for flash messages

=======
# preview_app.py
# TEMPORARY file only for testing my pages. NOT for GitHub.

from flask import Flask, render_template, request
from datetime import date
from billing import validate_booking, calculate_bill

# Create the Flask application
app = Flask(__name__)


# Route for the home page (web address: /)
>>>>>>> origin/member2-booking
@app.route("/")
def index():
    return render_template("index.html")

<<<<<<< HEAD
=======

# Route for the services page (web address: /services)
>>>>>>> origin/member2-booking
@app.route("/services")
def services():
    return render_template("services.html")

<<<<<<< HEAD
@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        flash("Booking received! (preview mode, not saved)")
        return redirect(url_for("booking"))
    return render_template("booking.html")

if __name__ == "__main__":
    app.run(debug=True)
=======

# methods=["GET", "POST"] lets this route open the page (GET)
# and also receive the submitted form (POST)
@app.route("/booking", methods=["GET", "POST"])
def booking():
    selected_service = request.args.get("service", "")
    today = date.today().isoformat()
    errors = []     # error messages to show on the page
    total = None    # the bill, only filled when the form is valid

    # The form was submitted
    if request.method == "POST":
        selected_service = request.form.get("service", "")

        # Use my function from billing.py to check the data
        is_valid, errors = validate_booking(request.form)

        if is_valid:
            # The form sends text, so convert quantity to a number first
            quantity = float(request.form["quantity"])
            total = calculate_bill(request.form["service"], quantity)

    return render_template("booking.html", selected_service=selected_service,
                           today=today, errors=errors, total=total)

# The navbar also needs these two names, so we add simple placeholders
@app.route("/tracking")
def tracking():
    return "Tracking page - coming soon"


@app.route("/dashboard")
def dashboard():
    return "Dashboard page - coming soon"


# This runs the website only when we start this file directly.
# debug=True shows helpful error messages and reloads when we save.
# port=5001 is used because Mac often uses port 5000 for itself.
if __name__ == "__main__":
    app.run(debug=True, port=5001)
>>>>>>> origin/member2-booking
