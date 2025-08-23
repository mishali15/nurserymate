import sqlite3
import os

def update_image_paths():
    # Connect to the database
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    
    # Get all plants with their current image URLs
    c.execute("SELECT id, scientific_name, image_url FROM plants")
    plants = c.fetchall()
    
    print("Current plants in database:")
    for plant in plants:
        plant_id, scientific_name, current_url = plant
        print(f"ID: {plant_id}, Name: {scientific_name}, Current URL: {current_url}")
    
    # Ask user for confirmation
    response = input("\nDo you want to update image paths to local files? (yes/no): ")
    
    if response.lower() == 'yes':
        # Update each plant's image_url to use local path
        for plant in plants:
            plant_id, scientific_name, current_url = plant
            
            # Create a filename from the scientific name
            # Replace spaces and special characters with underscores
            filename = scientific_name.lower().replace(' ', '_').replace('.', '').replace("'", "") + '.jpg'
            local_path = f"/static/images/{filename}"
            
            # Update the database
            c.execute("UPDATE plants SET image_url = ? WHERE id = ?", (local_path, plant_id))
            print(f"Updated {scientific_name}: {current_url} -> {local_path}")
        
        # Commit changes
        conn.commit()
        print("\nDatabase updated successfully!")
    else:
        print("Update cancelled.")
    
    conn.close()

if __name__ == "__main__":
    update_image_paths()
