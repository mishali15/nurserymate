# Application: NurseryMate
# Purpose: Plant recommendation system with database management capabilities
# Features:
#   - User authentication (admin)
#   - Plant data management (add/remove, view, query)
#   - Dynamic recommendations
#   - PDF plant care summary generation
# Data:
#   - SQLite database 'plants.db'
#   - Table: plants(
#       id INTEGER PRIMARY KEY AUTOINCREMENT,
#       scientific_name TEXT, common_name TEXT, flowering_time TEXT,
#       height TEXT, ecological_function TEXT, sunlight TEXT, water_level TEXT,
#       salt_wind_tolerance TEXT, type TEXT, planting_space TEXT,
#       image_url TEXT, soil_type TEXT
#     )
# Structure:
#   - Flask app with route functions (event-driven)
#   - Helper functions for DB access/validation
#   - Data structures: dict (records/form/session), list (collections), BytesIO (PDF)

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from werkzeug.utils import secure_filename
import os
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Data type: str (used by Flask session signing)

# --- Admin credentials (Data type: str) ---
valid_username = "admin"
valid_password = "password123"

# ------------------------------------------------------------
# Function: get_all_plants
# Purpose: Retrieve all plants from the database
# Returns: list[dict] -> each dict is a plant record for easy template rendering
# Control structures:
#   - Sequence: connect → query → fetch → close
#   - Iteration: build list of dicts from fetched rows
# Data structures/types:
#   - SQLite rows (tuple) → converted to dict
#   - list (collection of plant dicts), dict (field -> value)
# ------------------------------------------------------------
def get_all_plants():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, image_url, soil_type FROM plants")
    plants = c.fetchall()
    conn.close()
    
    plant_list = []
    for p in plants:  # Iteration over query results
        plant_list.append({
            "id": p[0],
            "scientific_name": p[1],
            "common_name": p[2],
            "flowering_time": p[3],
            "height": p[4],
            "ecological_function": p[5],
            "sunlight": p[6],
            "water_level": p[7],
            "salt_wind_tolerance": p[8],
            "type": p[9],
            "planting_space": p[10],
            "image_url": p[11],
            "soil_type": p[12]
        })
    return plant_list

# ------------------------------------------------------------
# Function: add_plant
# Purpose: Validate and insert a new plant
# Inputs: all fields as str; height validated as numeric (float) then stored with unit suffix
# Returns: None
# Control structures:
#   - Selection: presence checks; numeric range validation; error handling via exceptions
# Data types/structures:
#   - float(height) for validation (range 0–100), then str with "m" appended for storage
#   - SQLite parameterized INSERT (prevents injection)
# Why height as TEXT: keeps display-friendly "Xm" while still validating numerically
# ------------------------------------------------------------
def add_plant(scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type):
    # Selection: existence check for all fields
    if not all([scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type]):
        raise ValueError("All fields must be provided.")
    
    # Selection: numeric validation and range checking
    try:
        height_value = float(height)
        if height_value < 0 or height_value > 100:
            raise ValueError("Height must be between 0 and 100 meters.")
    except (ValueError, TypeError):
        raise ValueError("Height must be a valid number.")

    # Store as TEXT with unit suffix for consistent display
    height_str = f"{height_value}m"

    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO plants (scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, image_url, soil_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (scientific_name, common_name, flowering_time, height_str, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type)
    )
    conn.commit()
    conn.close()

# ------------------------------------------------------------
# Function: get_plant_by_id
# Purpose: Fetch a plant by its integer ID
# Returns: dict | None
# Control structures:
#   - Selection: validate plant_id; return None if invalid/not found
# Data types/structures:
#   - int (plant_id), tuple (row), dict (mapped record)
# ------------------------------------------------------------
def get_plant_by_id(plant_id):
    # Selection: guard against invalid IDs
    if not isinstance(plant_id, int) or plant_id <= 0:
        return None
    
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, image_url, soil_type FROM plants WHERE id = ?", (plant_id,))
    plant = c.fetchone()
    conn.close()
    
    if plant:  # Selection: exist/not-exist
        return {
            "id": plant[0],
            "scientific_name": plant[1],
            "common_name": plant[2],
            "flowering_time": plant[3],
            "height": plant[4],
            "ecological_function": plant[5],
            "sunlight": plant[6],
            "water_level": plant[7],
            "salt_wind_tolerance": plant[8],
            "type": plant[9],
            "planting_space": plant[10],
            "image_url": plant[11],
            "soil_type": plant[12]
        }
    return None

# ------------------------------------------------------------
# Function: remove_plant
# Purpose: Delete a plant by ID
# Control structures:
#   - Sequence: connect → delete → commit → close
# Data types:
#   - int (plant_id)
# ------------------------------------------------------------
def remove_plant(plant_id):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
    conn.commit()
    conn.close()

# ------------------------------------------------------------
# Function: query_plants
# Purpose: Filter plants according to user criteria
# Returns: list[dict] with minimal fields (id, scientific_name, image_url)
# Control structures:
#   - Sequence: fetch all → filter → return filtered
#   - Iteration: over all plants; per-plant evaluation
#   - Selection: multiple conditional checks inside matches()
# Data structures/types:
#   - dict form_data (criteria)
#   - dict value_mappings (nested dict[str -> list[str]] for keyword matching)
#   - list comprehension to produce filtered list
#   - floats/ints not required here; strings compared case-insensitively
# ------------------------------------------------------------
def query_plants(form_data):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, image_url, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, soil_type FROM plants")
    plants = c.fetchall()
    print(f"Total plants fetched from database: {len(plants)}")

    def matches(plant):
        (id, scientific_name, image_url, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, soil_type) = plant
        match_count = 0     # Data type: int
        total_criteria = 0  # Data type: int

        # Data structure: nested dict of lists for flexible mapping
        value_mappings = {
            "water_level": {
                "Dry or drought-prone": ["dry", "drought"],
                "Moderate moisture (well-watered)": ["moderate", "well-watered"],
                "Wet or swampy": ["wet", "swampy"]
            },
            "salt_wind_tolerance": {
                "Yes — coastal or exposed site": ["yes", "coastal"],
                "No — sheltered inland site": ["no", "sheltered"]
            },
            "type": {
                "Groundcover or creeping": ["groundcover", "creeping"],
                "Tufting or grass-like": ["tufting", "grass"],
                "Small herb or dainty flower": ["small herb", "dainty flower", "herb"],
                "Shrub or tree": ["shrub", "tree"]
            }
        }

        # Selection blocks for each optional criterion; string normalization for robust matching
        if form_data.get("flowering_time"):
            total_criteria += 1
            if form_data["flowering_time"].lower() in flowering_time.lower():
                match_count += 1
        if form_data.get("ecological_function"):
            total_criteria += 1
            if form_data["ecological_function"].lower() in ecological_function.lower():
                match_count += 1
        if form_data.get("sunlight"):
            total_criteria += 1
            form_sunlight = form_data["sunlight"].lower()
            plant_sunlight = sunlight.lower()
            if ("full sun" in form_sunlight and "full sun" in plant_sunlight) or \
               ("partial shade" in form_sunlight and ("partial" in plant_sunlight or "shade" in plant_sunlight)) or \
               ("full shade" in form_sunlight and ("shade" in plant_sunlight or "partial" in plant_sunlight)):
                match_count += 1
        if form_data.get("water_level"):
            total_criteria += 1
            form_water = form_data["water_level"].lower()
            plant_water = water_level.lower()
            if form_water in value_mappings["water_level"]:
                for keyword in value_mappings["water_level"][form_water]:  # Iteration over synonyms
                    if keyword in plant_water:
                        match_count += 1
                        break
        if form_data.get("salt_wind_tolerance"):
            total_criteria += 1
            form_tolerance = form_data["salt_wind_tolerance"].lower()
            plant_tolerance = salt_wind_tolerance.lower()
            if "yes" in form_tolerance and ("yes" in plant_tolerance or "coastal" in plant_tolerance):
                match_count += 1
            elif "no" in form_tolerance and ("no" in plant_tolerance or "sheltered" in plant_tolerance):
                match_count += 1
        if form_data.get("type"):
            total_criteria += 1
            form_type = form_data["type"].lower()
            plant_type = type_.lower()
            if form_type in value_mappings["type"]:
                for keyword in value_mappings["type"][form_type]:  # Iteration
                    if keyword in plant_type:
                        match_count += 1
                        break
        if form_data.get("planting_space"):
            total_criteria += 1
            form_space = form_data["planting_space"].lower()
            plant_space = planting_space.lower()
            if ("small" in form_space and "small" in plant_space) or \
               ("medium" in form_space and "medium" in plant_space) or \
               ("large" in form_space and "large" in plant_space) or \
               ("low" in form_space and "low" in plant_space):
                match_count += 1
        if form_data.get("soil_type"):
            total_criteria += 1
            form_soil = form_data["soil_type"].lower()
            plant_soil = soil_type.lower()
            if form_soil in plant_soil:
                match_count += 1

        # Selection: no criteria means match all; otherwise threshold-based match
        if total_criteria == 0:
            return True
        return (match_count / total_criteria) >= 0.4

    # Iteration via list comprehension filters only matching plants and maps to dicts
    filtered_plants = [
        {"id": p[0], "scientific_name": p[1], "image_url": p[2]}
        for p in plants if matches(p)
    ]
    
    conn.close()
    return filtered_plants

# ------------------------------------------------------------
# Route: Home page
# URL: "/"
# Method(s): GET
# Purpose: Serve the landing page
# Control structures: straight sequence (render template)
# Data structures: template context dict (empty here)
# ------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ------------------------------------------------------------
# Route: Plant selection form
# URL: "/form"
# Method(s): GET, POST
# Purpose: Show form (GET); collect criteria and redirect to /results (POST)
# Control structures:
#   - Selection: branch by request.method
#   - Sequence: collect fields → redirect with query params
# Data structures:
#   - dict form_data (criteria captured from form inputs)
# ------------------------------------------------------------
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":  # Selection: POST-handling branch
        form_data = {
            "soil_type": request.form.get("soil_type"),
            "sunlight": request.form.get("sunlight"),
            "water_level": request.form.get("water_level"),
            "salt_wind_tolerance": request.form.get("salt_wind_tolerance"),
            "type": request.form.get("type"),
            "ecological_function": request.form.get("ecological_function"),
            "planting_space": request.form.get("planting_space"),
        }
        return redirect(url_for("results", **form_data))  # Sequence: build URL with dict unpacking
    return render_template("form.html")

# ------------------------------------------------------------
# Route: Plant details
# URL: "/plant/<int:plant_id>"
# Method(s): GET
# Purpose: Display full details for a single plant
# Control structures:
#   - Sequence: fetch record → render template
# Data types/structures:
#   - int path parameter (plant_id)
#   - dict plant record passed to template
# ------------------------------------------------------------
@app.route("/plant/<int:plant_id>")
def plant_details(plant_id):
    plant = get_plant_by_id(plant_id)
    return render_template("plant_details.html", plant=plant)

# ------------------------------------------------------------
# Route: Results
# URL: "/results"
# Method(s): GET
# Purpose: Run query based on criteria from query string and show results
# Control structures:
#   - Sequence: collect args → query → render
# Data structures:
#   - dict form_data; list[dict] plants
# ------------------------------------------------------------
@app.route("/results", methods=["GET"])
def results():
    form_data = {
        "soil_type": request.args.get("soil_type"),
        "sunlight": request.args.get("sunlight"),
        "water_level": request.args.get("water_level"),
        "salt_wind_tolerance": request.args.get("salt_wind_tolerance"),
        "type": request.args.get("type"),
        "ecological_function": request.args.get("ecological_function"),
        "planting_space": request.args.get("planting_space"),
    }
    plants = query_plants(form_data)
    return render_template("results_final.html", plants=plants)

# ------------------------------------------------------------
# Route: Login
# URL: "/login"
# Method(s): GET, POST
# Purpose: Authenticate admin user
# Control structures:
#   - Selection: branch by method (GET vs POST)
#   - Selection: credential check; set session flag; handle error
# Data structures/types:
#   - dict-like session for 'logged_in' flag (bool-like)
#   - str username/password from form
# ------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == valid_username and password == valid_password:  # Selection
            session['logged_in'] = True
            return redirect(url_for("adminDashboard"))
        else:
            error = "Invalid login credentials. Please try again."
            return render_template("login.html", error=error)
    return render_template("login.html")

# ------------------------------------------------------------
# Route: Admin dashboard
# URL: "/adminDashboard"
# Method(s): GET, POST
# Purpose: Manage plants (add/remove) and list all plants
# Control structures:
#   - Selection: require login; redirect if not authenticated
#   - Selection: POST vs GET
#   - Selection: handle remove vs add_plant actions
#   - Selection: presence of image file; ensure path normalization
# Data structures/types:
#   - dict-like session; form fields (str)
#   - file upload object (Werkzeug FileStorage) → saved as path str in DB
#   - list[dict] plants for template
# ------------------------------------------------------------
@app.route("/adminDashboard", methods=["GET", "POST"])
def adminDashboard():
    if not session.get('logged_in'):  # Selection: access control
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    if request.method == "POST":  # Selection: request method
        if "remove_id" in request.form:  # Selection: removal branch
            plant_id = request.form.get("remove_id")
            if plant_id:
                remove_plant(int(plant_id))
                flash("Plant removed successfully.")
            else:
                flash("No plant ID provided. Please select a plant to remove.")
        elif "add_plant" in request.form:  # Selection: add branch
            # Extract form inputs (Data types: str for all)
            scientific_name = request.form.get("scientific_name")
            common_name = request.form.get("common_name")
            flowering_time = request.form.get("flowering_time")
            height = request.form.get("height")
            ecological_function = request.form.get("ecological_function")
            sunlight = request.form.get("sunlight")
            water_level = request.form.get("water_level")
            salt_wind_tolerance = request.form.get("salt_wind_tolerance")
            type_ = request.form.get("type")
            planting_space = request.form.get("planting_space")
            image_file = request.files.get("image_file")  # FileStorage object

            # Selection: handle image upload if provided
            if image_file:
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join('static/images', image_filename))
                image_url = f"/static/images/{image_filename}"
            else:
                image_url = None  # Data type: None | str

            # Selection: ensure path normalization
            if image_url and not image_url.startswith('/static/'):
                image_url = f"/static/{image_url}"

            soil_type = request.form.get("soil_type")

            # Selection: wrap add_plant in try/except to surface validation errors to UI
            try:
                add_plant(scientific_name, common_name, flowering_time, height, ecological_function,
                          sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type)
                flash("Plant added successfully.")
            except ValueError as e:
                flash(f"Error adding plant: {str(e)}")

    plants = get_all_plants()  # list[dict]
    return render_template("dashboard.html", plants=plants)

# ------------------------------------------------------------
# Route: Logout
# URL: "/logout"
# Method(s): GET
# Purpose: Clear session and redirect to login
# Control structures:
#   - Sequence: clear session → redirect
# Data structures:
#   - session (dict-like) mutated
# ------------------------------------------------------------
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ------------------------------------------------------------
# Route: Generate plant care summary (PDF)
# URL: "/generate_summary/<int:plant_id>"
# Method(s): POST
# Purpose: Build a PDF in-memory and return as download
# Control structures:
#   - Selection: validate ID; 404 if not found
#   - Sequence: fetch → compose story → build PDF → return file
# Data structures/types:
#   - BytesIO buffer (in-memory file)
#   - tuple row from DB; accessed by index
#   - reportlab Flowables: Paragraph, Spacer
# ------------------------------------------------------------
@app.route("/generate_summary/<int:plant_id>", methods=["POST"])
def generate_summary(plant_id):
    if not isinstance(plant_id, int) or plant_id <= 0:  # Selection
        return "Invalid plant ID", 400
    
    conn = sqlite3.connect("plants.db")
    c = conn.cursor()
    c.execute("SELECT scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space FROM plants WHERE id=?", (plant_id,))
    plant = c.fetchone()
    conn.close()

    if not plant:  # Selection
        return "Plant not found", 404

    buffer = io.BytesIO()  # Data type: in-memory bytes buffer
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []  # list of Flowables

    story.append(Paragraph(f"<b>{plant[1]} ({plant[0]})</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Flowering Time:</b> {plant[2]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Height:</b> {plant[3]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Ecological Function:</b> {plant[4]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Sunlight:</b> {plant[5]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Water Level:</b> {plant[6]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Salt/Wind Tolerance:</b> {plant[7]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Type:</b> {plant[8]}", styles["Normal"]))
    story.append(Paragraph(f"<b>Planting Space:</b> {plant[9]}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{plant[1]}_care_summary.pdf", mimetype="application/pdf")

# ------------------------------------------------------------
# Function: init_db
# Purpose: Create plants table if it doesn't exist
# Control structures:
#   - Sequence: connect → execute DDL → commit → close
# Data structures/types:
#   - SQLite schema (TEXT columns for categorical/flexible text; height TEXT for unit-suffixed values)
#   - INTEGER PRIMARY KEY AUTOINCREMENT for unique IDs
# ------------------------------------------------------------
def init_db():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scientific_name TEXT NOT NULL,
            common_name TEXT,
            flowering_time TEXT,
            height TEXT,
            ecological_function TEXT,
            sunlight TEXT,
            water_level TEXT,
            salt_wind_tolerance TEXT,
            type TEXT,
            planting_space TEXT,
            image_url TEXT,
            soil_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ------------------------------------------------------------
# App entrypoint
# Control structures:
#   - Sequence: init DB → run app (debug mode)
# ------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
