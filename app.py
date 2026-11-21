# app.py
# Member 3: creates the Flask app and its routes for FreshFold Laundry

from flask import Flask, render_template, request, redirect, url_for
import storage
import reports  # our report functions # our own CSV functions
from fake_billing import (
    validate_booking,
    generate_confirmation,
)  # TEMPORARY: replace with Member 2's billing.py later

app = Flask(__name__)  # create the Flask application


@app.route("/")
def index():
    """Home page (Member 1's index.html)."""
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Admin dashboard. POST changes an order's status, GET shows the page."""
    if request.method == "POST":
        order_id = request.form.get("order_id", "")  # which order
        new_status = request.form.get("new_status", "")  # which status
        storage.update_status(order_id, new_status)  # save the change
        return redirect(url_for("dashboard"))  # reload the dashboard

    summary = reports.get_summary()  # all the numbers in one dictionary
    orders = storage.get_all_orders()  # list of every order for the table
    return render_template(
        "dashboard.html",
        summary=summary,
        orders=orders,
        statuses=storage.STATUSES,
    )


@app.route("/services")
def services():
    """Services page (Member 1's services.html)."""
    return render_template("services.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():
    """GET: show the booking form. POST: validate, save, then show tracking."""
    errors = []  # messages to show if the form is wrong

    if request.method == "POST":
        form_data = request.form  # what the user typed
        is_valid, errors = validate_booking(form_data)  # Member 2's checker

        if is_valid:
            details = generate_confirmation(form_data)  # cleaned data + total price
            saved = storage.save_order(
                {
                    "full_name": details["full_name"],
                    "phone": details["phone"],
                    "service": details["service"],
                    "quantity": details["quantity"],
                    "total": details["total"],
                    "pickup_date": details["pickup_date"],
                    "pickup_time": details["pickup_time"],
                    "instructions": details["instructions"],
                }
            )
            # Send the user to the tracking page for their new order
            return redirect(url_for("tracking", order_id=saved["order_id"]))

    # GET visit, or POST with errors: show the form again
    selected_service = request.args.get("service", "")  # from /booking?service=washing
    return render_template(
        "booking_test.html", errors=errors, selected_service=selected_service
    )


@app.route("/tracking")
def tracking():
    """Show the tracking page, and the order's progress if an ID was searched."""
    order_id = request.args.get("order_id", "").strip()  # text from the address bar

    order = None  # no order yet
    current_step = -1  # -1 means "no step highlighted"
    searched = False  # did the user search for something?

    if order_id != "":
        searched = True
        order = storage.get_order(order_id)  # dictionary or None
        if order is not None:
            # position of this order's status: 0, 1, 2 or 3
            current_step = storage.STATUSES.index(order["status"])

    return render_template(
        "tracking.html",
        order=order,
        searched=searched,
        current_step=current_step,
        statuses=storage.STATUSES,
    )


# Runs only when you start this file directly
if __name__ == "__main__":
    app.run(debug=True)  # debug=True shows helpful error messages
