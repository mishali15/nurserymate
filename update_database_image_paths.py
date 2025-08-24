import sqlite3

def update_database_image_paths():
    """Update database image paths to use snake_case naming conventions"""
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    
    # Mapping of old image paths to new snake_case paths
    image_updates = [
        # Format: (old_filename, new_filename)
        ("Acacia_dealbata.jpg", "acacia_dealbata.jpg"),
        ("austrostipa_scabra_ssp._falcata.jpg", "austrostipa_scabra_ssp_falcata.jpg"),
        ("brachyscome_basaltica_var.jpg", "brachyscome_basaltica.jpg"),
        ("bulbine_semibarbarta.jpg", "bulbine_semibarbata.jpg"),
        ("sarcocornia-quinqueflora.jpg", "sarcocornia_quinqueflora.jpg")
    ]
    
    print("Updating database image paths to snake_case:")
    
    for old_name, new_name in image_updates:
        # Update database records
        old_path = f"/static/images/{old_name}"
        new_path = f"/static/images/{new_name}"
        
        c.execute("UPDATE plants SET image_url = ? WHERE image_url = ?", (new_path, old_path))
        updated_count = c.rowcount
        
        if updated_count > 0:
            print(f"✅ Updated {updated_count} records: {old_name} -> {new_name}")
        else:
            print(f"⚠️  No records found for: {old_name}")
    
    conn.commit()
    conn.close()
    print("Database update completed!")

if __name__ == "__main__":
    update_database_image_paths()
