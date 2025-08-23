import sqlite3

def fix_acaena_image():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    
    # Check current image URL for Acaena novae-zealandiae
    c.execute("SELECT id, scientific_name, image_url FROM plants WHERE scientific_name LIKE '%Acaena novae-zealandiae%'")
    plant = c.fetchone()
    
    if plant:
        plant_id, scientific_name, current_url = plant
        print(f"Current: {scientific_name} -> {current_url}")
        
        # Update to use the correct local path
        correct_path = "/static/images/acaena_novae-zelandiae.jpg"
        c.execute("UPDATE plants SET image_url = ? WHERE id = ?", (correct_path, plant_id))
        conn.commit()
        print(f"Updated to: {correct_path}")
    else:
        print("Acaena novae-zealandiae not found in database")
    
    conn.close()

if __name__ == "__main__":
    fix_acaena_image()
