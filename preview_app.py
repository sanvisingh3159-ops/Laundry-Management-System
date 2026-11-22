from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "preview-key"      # needed for flash messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        flash("Booking received! (preview mode, not saved)")
        return redirect(url_for("booking"))
    return render_template("booking.html")

# TEMPORARY placeholders: replace with render_template(...) once the pages exist
@app.route("/tracking", methods=["GET", "POST"])
def tracking():
    return "<h2>Tracking page coming soon</h2><a href='/'>Back to Home</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    return "<h2>Login page coming soon</h2><a href='/'>Back to Home</a>"

@app.route("/admin")
def admin():
    return "<h2>Admin dashboard coming soon</h2><a href='/'>Back to Home</a>"

if __name__ == "__main__":
    app.run(debug=True)