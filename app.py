from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

validUsername = "admin"
validPassword = "password123"

def get_all_plants():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, common_name, flowering_time, height, growing_requirements FROM plants")
    plants = c.fetchall()
    conn.close()
    return plants

def add_plant(scientific_name, common_name, flowering_time, height, growing_requirements):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO plants (scientific_name, common_name, flowering_time, height, growing_requirements) VALUES (?, ?, ?, ?, ?)",
        (scientific_name, common_name, flowering_time, height, growing_requirements)
    )
    conn.commit()
    conn.close()

def remove_plant(plant_id):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
    conn.commit()
    conn.close()

def query_plants(form_data):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    query = "SELECT scientific_name, common_name, flowering_time, height, growing_requirements FROM plants"
    c.execute(query)
    plants = c.fetchall()
    def matches(plant):
        scientific_name, common_name, flowering_time, height, growing_requirements = plant
        gr = growing_requirements.lower()
        match_count = 0
        total_criteria = 8
        # ...matching logic unchanged...
        # Soil type matching
        soil_type = form_data.get("soil_type", "").lower()
        if soil_type:
            if soil_type == "dry, sandy or loamy" and any(x in gr for x in ["dry", "sandy", "loam", "loamy"]):
                match_count += 1
            elif soil_type == "heavy, clay or waterlogged" and any(x in gr for x in ["clay", "waterlogged", "heavy"]):
                match_count += 1
            elif soil_type == "moist, well-drained" and any(x in gr for x in ["moist", "well-drained", "well drained"]):
                match_count += 1
            elif soil_type == "saline or coastal" and any(x in gr for x in ["saline", "coastal", "salt"]):
                match_count += 1
        sunlight = form_data.get("sunlight", "").lower()
        if sunlight:
            if sunlight == "full sun (most of the day)" and "full sun" in gr:
                match_count += 1
            elif sunlight == "partial shade (some sun, some shade)" and any(x in gr for x in ["partial shade", "part shade", "semi-shade", "semi shade"]):
                match_count += 1
            elif sunlight == "full shade (very little direct sun)" and any(x in gr for x in ["full shade", "shade"]):
                match_count += 1
        water = form_data.get("water_availability", "").lower()
        if water:
            if water == "dry or drought-prone" and any(x in gr for x in ["dry", "drought"]):
                match_count += 1
            elif water == "moderate moisture (well-watered)" and any(x in gr for x in ["moderate moisture", "well-watered", "well watered", "moist"]):
                match_count += 1
            elif water == "wet or swampy" and any(x in gr for x in ["wet", "swamp", "waterlogged", "aquatic"]):
                match_count += 1
        salt = form_data.get("salt_wind_tolerance", "").lower()
        if salt:
            if salt == "yes — coastal or exposed site" and any(x in gr for x in ["salt", "coastal", "wind"]):
                match_count += 1
            elif salt == "no — sheltered inland site" and not any(x in gr for x in ["salt", "coastal", "wind"]):
                match_count += 1
        plant_type = form_data.get("plant_type", "").lower()
        if plant_type:
            if plant_type == "groundcover or creeping" and any(x in gr for x in ["groundcover", "creeping", "mat-forming", "low maintenance groundcover"]):
                match_count += 1
            elif plant_type == "tufting or grass-like" and any(x in gr for x in ["grass", "tufting", "spear grass", "wallaby grass"]):
                match_count += 1
            elif plant_type == "small herb or dainty flower" and any(x in gr for x in ["herb", "flower", "lily", "daisy", "everlasting"]):
                match_count += 1
            elif plant_type == "shrub or tree" and any(x in gr for x in ["shrub", "tree", "wattle", "banksia", "acacia"]):
                match_count += 1
        eco_func = form_data.get("ecological_function", "").lower()
        if eco_func:
            if eco_func == "attract birds and butterflies" and any(x in gr for x in ["attract", "birds", "butterflies", "wildlife"]):
                match_count += 1
            elif eco_func == "provide food (e.g., berries)" and any(x in gr for x in ["food", "berries"]):
                match_count += 1
            elif eco_func == "structural/visual interest" and any(x in gr for x in ["structural", "visual", "aesthetic", "flower", "fragrant"]):
                match_count += 1
            elif eco_func == "low-maintenance only" and any(x in gr for x in ["low maintenance", "low-maintenance", "drought-tolerant", "drought tolerant"]):
                match_count += 1
        maintenance = form_data.get("maintenance_level", "").lower()
        if maintenance:
            if maintenance == "low (minimal pruning, drought-tolerant)" and any(x in gr for x in ["low maintenance", "drought-tolerant", "minimal pruning"]):
                match_count += 1
            elif maintenance == "medium (occasional watering and pruning)" and any(x in gr for x in ["moderate maintenance", "occasional watering", "pruning"]):
                match_count += 1
            elif maintenance == "high (regular watering, fertilising, pruning)" and any(x in gr for x in ["regular watering", "fertilising", "pruning"]):
                match_count += 1
        space = form_data.get("planting_space", "").lower()
        if space:
            if space == "small pot / container" and any(x in gr for x in ["small", "container", "pot"]):
                match_count += 1
            elif space == "small garden bed (<1m spread)" and any(x in gr for x in ["small garden", "<1m", "small"]):
                match_count += 1
            elif space == "medium garden area (1–3m spread)" and any(x in gr for x in ["medium garden", "1–3m", "1-3m"]):
                match_count += 1
            elif space == "large area (>3m spread)" and any(x in gr for x in ["large", ">3m", "3m"]):
                match_count += 1
        return match_count >= 3
    filtered_plants = [ 
        {
            "scientific_name": p[0],
            "common_name": p[1],
            "flowering_time": p[2],
            "height": p[3],
            "growing_requirements": p[4]
        }
        for p in plants if matches(p)
    ]
    conn.close()
    return filtered_plants

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
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
        return redirect(url_for("results", **form_data))
    return render_template("form.html")

@app.route("/results")
def results():
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
    matching_plants = query_plants(form_data)
    return render_template("results.html", form_data=form_data, plants=matching_plants)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == validUsername and password == validPassword:
            session['logged_in'] = True
            return redirect(url_for("adminDashboard"))
        else:
            error = "Invalid login credentials. Please try again."
    return render_template("login.html", error=error)

@app.route("/adminDashboard", methods=["GET", "POST"])
def adminDashboard():
    if not session.get('logged_in'):
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    if request.method == "POST":
        if "remove_id" in request.form:
            plant_id = request.form.get("remove_id")
            remove_plant(plant_id)
        elif "add_plant" in request.form:
            scientific_name = request.form.get("scientific_name")
            common_name = request.form.get("common_name")
            flowering_time = request.form.get("flowering_time")
            height = request.form.get("height")
            growing_requirements = request.form.get("growing_requirements")
            add_plant(scientific_name, common_name, flowering_time, height, growing_requirements)

    plants = get_all_plants()
    return render_template("dashboard.html", plants=plants)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def init_db():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scientific_name TEXT NOT NULL,
            common_name TEXT NOT NULL,
            flowering_time TEXT,
            height TEXT,
            growing_requirements TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
