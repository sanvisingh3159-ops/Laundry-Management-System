from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

# Placeholders so the navbar links work until teammates finish their pages
@app.route("/booking")
def booking():
    return "Booking page - Member 2 will build this"

@app.route("/tracking")
def tracking():
    return "Tracking page - Member 3 will build this"

if __name__ == "__main__":
    app.run(debug=True)