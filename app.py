from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

validUsername = "admin"
validPassword = "password123"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Collect form data
        form_data = {
            "soil_type": request.form.get("soil_type"),
            "sunlight": request.form.get("sunlight"),
            "water_availability": request.form.get("water_availability"),
            "salt_wind_tolerance": request.form.get("salt_wind_tolerance"),
            "plant_type": request.form.get("plant_type"),
            "ecological_function": request.form.get("ecological_function"),
            "maintenance_level": request.form.get("maintenance_level"),
            "planting_space": request.form.get("planting_space"),
        }
        print("Received form data:", form_data)
        # Redirect to results page with the collected data
        return redirect(url_for("results", **form_data))
    return render_template("form.html")

@app.route("/results")
def results():
    # Get form data from query parameters
    form_data = {
        "soil_type": request.args.get("soil_type"),
        "sunlight": request.args.get("sunlight"),
        "water_availability": request.args.get("water_availability"),
        "salt_wind_tolerance": request.args.get("salt_wind_tolerance"),
        "plant_type": request.args.get("plant_type"),
        "ecological_function": request.args.get("ecological_function"),
        "maintenance_level": request.args.get("maintenance_level"),
        "planting_space": request.args.get("planting_space"),
    }
    return render_template("results.html", form_data=form_data)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        if username == validUsername and password == validPassword:
            return redirect(url_for("adminDashboard"))
        else:
            error = "Invalid login credentials. Please try again."
    
    return render_template("login.html", error=error)

@app.route("/adminDashboard")
def adminDashboard():
    return "<h2>Admin Dashboard - Plant Management System</h2><p>Under Construction: This area will contain tools for managing plant recommendations and system data.</p>"

if __name__ == "__main__":
    app.run(debug=True)
