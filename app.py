# Application: NurseryMate
# Purpose: Plant recommendation system with database management capabilities
# Features: User authentication, plant data management, dynamic recommendations
# Data: Uses SQLite database 'plants.db' to store plant information
# Structure: Flask-based web application with routes for different functionalities

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Admin credentials for dashboard access

valid_username = "admin"
valid_password = "password123"

# Function: get_all_plants
# Purpose: Retrieve all plants from the database
# Output: List of dictionaries containing plant details

def get_all_plants():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, image_url, soil_type FROM plants")
    plants = c.fetchall()
    conn.close()
    
    
    plant_list = []
    for p in plants:
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

# Function: add_plant
# Purpose: Add a new plant to the database
# Input: 
#   scientific_name (str): The scientific name of the plant
#   common_name (str): The common name of the plant
#   flowering_time (str): The flowering time of the plant
#   height (str): The height of the plant
#   ecological_function (str): The ecological function of the plant
#   sunlight (str): The sunlight requirements of the plant
#   water_level (str): The water level requirements of the plant
#   salt_wind_tolerance (str): The salt and wind tolerance of the plant
#   type_ (str): The type of the plant
#   planting_space (str): The planting space required for the plant
#   image_url (str): The URL of the plant's image
#   soil_type (str): The soil type suitable for the plant
# Output: None (just stored in database)

def add_plant(scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO plants (scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, image_url, soil_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type)
    )
    conn.commit()
    conn.close()

# Function: get_plant_by_id
# Purpose: Fetch a specific plant by its ID from the database
# Input: plant_id (int): The ID of the plant to fetch
# Output: A dictionary containing plant details if found, else None

def get_plant_by_id(plant_id):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, image_url, soil_type FROM plants WHERE id = ?", (plant_id,))
    plant = c.fetchone()
    conn.close()
    
    if plant:
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

# Function: remove_plant
# Purpose: Remove a plant from the database by its ID
# Input: plant_id (int): The ID of the plant to remove

def remove_plant(plant_id):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
    conn.commit()
    conn.close()

# Function: query_plants
# Purpose: Query plants based on user input criteria and return matching results
# Input: form_data (dict) = a dictionary containing user input criteria
# Output: list: A list of dictionaries containing matching plant details

def query_plants(form_data):
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    c.execute("SELECT id, scientific_name, image_url, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type, planting_space, soil_type FROM plants")
    plants = c.fetchall()
    print(f"Total plants fetched from database: {len(plants)}")

    def matches(plant):
        (id, scientific_name, image_url, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, soil_type) = plant
        match_count = 0
        total_criteria = 0

        # Values in the form are mapped to keywords for more flexible matching. 
        # E.g., "Dry or drought-prone" can match "dry" or "drought" in the database
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

        # Control structure: Conditional statements to check each criterion
        # Input: form_data (dict): User input criteria
        # Output: Boolean indicating if plant matches criteria
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

            # Will allow for more flexible matching

            if ("full sun" in form_sunlight and "full sun" in plant_sunlight) or \
               ("partial shade" in form_sunlight and ("partial" in plant_sunlight or "shade" in plant_sunlight)) or \
               ("full shade" in form_sunlight and ("shade" in plant_sunlight or "partial" in plant_sunlight)):
                match_count += 1
        if form_data.get("water_level"):
            total_criteria += 1
            form_water = form_data["water_level"].lower()
            plant_water = water_level.lower()

            # Use mapping for water level

            if form_water in value_mappings["water_level"]:
                for keyword in value_mappings["water_level"][form_water]:
                    if keyword in plant_water:
                        match_count += 1
                        break
        if form_data.get("salt_wind_tolerance"):
            total_criteria += 1
            form_tolerance = form_data["salt_wind_tolerance"].lower()
            plant_tolerance = salt_wind_tolerance.lower()

            # Use mapping for tolerance

            if "yes" in form_tolerance and ("yes" in plant_tolerance or "coastal" in plant_tolerance):
                match_count += 1
            elif "no" in form_tolerance and ("no" in plant_tolerance or "sheltered" in plant_tolerance):
                match_count += 1
        if form_data.get("type"):
            total_criteria += 1
            form_type = form_data["type"].lower()
            plant_type = type_.lower()

            # Use mapping for plant type

            if form_type in value_mappings["type"]:
                for keyword in value_mappings["type"][form_type]:
                    if keyword in plant_type:
                        match_count += 1
                        break
        if form_data.get("planting_space"):
            total_criteria += 1
            form_space = form_data["planting_space"].lower()
            plant_space = planting_space.lower()

            # Flexible space matching

            if ("small" in form_space and "small" in plant_space) or \
               ("medium" in form_space and "medium" in plant_space) or \
               ("large" in form_space and "large" in plant_space) or \
               ("low" in form_space and "low" in plant_space):
                match_count += 1
        if form_data.get("soil_type"):
            total_criteria += 1
            form_soil = form_data["soil_type"].lower()
            plant_soil = soil_type.lower()

            # Flexible soil matching

            if form_soil in plant_soil:
                match_count += 1

        print(f"Checking plant: {scientific_name}, criteria: {form_data}, matches: {match_count}/{total_criteria}, total_criteria: {total_criteria}")
        print(f"Plant data: flowering_time={flowering_time}, ecological_function={ecological_function}, sunlight={sunlight}, water_level={water_level}, salt_wind_tolerance={salt_wind_tolerance}, type={type_}, planting_space={planting_space}, soil_type={soil_type}")
        
        # Or if no criteria were provided, return all plants
        # The plant should match at least 40% of the provided criteria to be included. 
        # This would ensure that plants are not excluded too strictly when multiple criteria are given.
        # Thus user will be provided with some sort of results.
        
        if total_criteria == 0:
            return True
        return (match_count / total_criteria) >= 0.4

    filtered_plants = [
        {
            "id": p[0],  # ID field
            "scientific_name": p[1],  # scientific_name field
            "image_url": p[2]  # image_url field
        }
        for p in plants if matches(p)
    ]
    
    # Debug: Print the filtered plants with their image URLs
    print(f"Filtered plants: {len(filtered_plants)}")
    for plant in filtered_plants:
        print(f"Plant: {plant['scientific_name']}, Image URL: {plant['image_url']}")
    
    conn.close()
    return filtered_plants

# Route: Home page
# Purpose: Serve the main landing page of the application
@app.route("/")
def home():
    return render_template("index.html")

# Route: Plant selection form
# Purpose: Handle plant selection form (GET for display, POST for form submission)
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        form_data = {
            "soil_type": request.form.get("soil_type"),
            "sunlight": request.form.get("sunlight"),
            "water_level": request.form.get("water_level"),
            "salt_wind_tolerance": request.form.get("salt_wind_tolerance"),
            "type": request.form.get("type"),
            "ecological_function": request.form.get("ecological_function"),
            "planting_space": request.form.get("planting_space"),
        }
        return redirect(url_for("results", **form_data))
    return render_template("form.html")

# Route: Plant details page
# Purpose: Display detailed information about a specific plant
@app.route("/plant/<int:plant_id>")
def plant_details(plant_id):
    plant = get_plant_by_id(plant_id)  # Fetch plant data from the database
    return render_template("plant_details.html", plant=plant)

# Route: Download plant care summary
# Purpose: Generate and download a text file with plant care information
@app.route("/download_care_summary/<int:plant_id>")
def download_care_summary(plant_id):
    plant = get_plant_by_id(plant_id)
    if plant:
        care_requirements = f"""
        Plant Care Summary for {plant['scientific_name']}:
        
        Sunlight: {plant['sunlight']}
        Water Level: {plant['water_level']}
        Soil Type: {plant['soil_type']}
        Ecological Function: {plant['ecological_function']}
        Planting Space: {plant['planting_space']}
        """
        response = make_response(care_requirements)
        response.headers["Content-Disposition"] = f"attachment; filename={plant['scientific_name']}_care_summary.txt"
        response.headers["Content-Type"] = "text/plain"
        return response

# Route: Plant recommendation results
# Purpose: Display plant recommendations based on user criteria from query parameters
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

# Route: Admin login
# Purpose: Handle admin authentication for dashboard access
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == valid_username and password == valid_password:
            session['logged_in'] = True
            return redirect(url_for("adminDashboard"))
        else:
            error = "Invalid login credentials. Please try again."
            return render_template("login.html", error=error)
    return render_template("login.html")

# Route: Admin dashboard
# Purpose: Provide admin interface for managing plant database (add/remove plants)
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
            ecological_function = request.form.get("ecological_function")
            sunlight = request.form.get("sunlight")
            water_level = request.form.get("water_level")
            salt_wind_tolerance = request.form.get("salt_wind_tolerance")
            type_ = request.form.get("type")
            planting_space = request.form.get("planting_space")
            image_url = request.form.get("image_url")
            soil_type = request.form.get("soil_type")
            add_plant(scientific_name, common_name, flowering_time, height, ecological_function, sunlight, water_level, salt_wind_tolerance, type_, planting_space, image_url, soil_type)

    plants = get_all_plants()
    return render_template("dashboard.html", plants=plants)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Function: init_db
# Purpose: Initialize the database by creating the plants table if it doesn't exist
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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)