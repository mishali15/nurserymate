import sqlite3
import os

def fix_specific_matches():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    
    # Problematic plants and their correct filenames
    fixes = [
        # Current filename vs what it should be
        ("acacia_pycnantha.jfif", "acacia_pycnantha.jpg"),
        ("acaena_novaezelandiae.jpg", "acaena_novae-zelandiae.jpg"),
        ("alisma_plantago_aquatica.jpg", "alisma_plantago-aquatica.jpg"),
        # New mappings for .jfif files
        ("austrostipa_gibbosa.jfif", "austrostipa_gibbosa.jpg"),
        ("austrostipa_scabra_ssp._falcata.jfif", "austrostipa_scabra_ssp.falcata.jpg"),
        ("austrostipa_setacea.jfif", "austrostipa_setacea.jpg"),
        ("baumea_articulata.jfif", "baumea_articulata.jpg"),
        ("sarcocornia.jfif", "sarcocornia_quinqueflora.jpg"),
        ("bothriochloa.jfif", "bothriochloa.jpg"),
        ("bulbine_semibarbata.jfif", "bulbine_semibarbata.jpg"),
        ("bursaria_spinosa_var._spinosa.jfif", "bursaria_spinosa.jpg"),
        ("carpobrotus_modestus.jfif", "carpobrotus_modestus.jpg"),
        ("amphibromus_ neesii.jpg", "amphibromus_neesii.jpg")  # Remove space
    ]
    
    print("Fixing specific image filename mismatches:")
    
    for current_filename, correct_filename in fixes:
        # Check if current file exists
        current_path = f"static/images/{current_filename}"
        correct_path = f"static/images/{correct_filename}"
        
        if os.path.exists(current_path):
            # Rename the file
            os.rename(current_path, correct_path)
            print(f"✅ Renamed: {current_filename} -> {correct_filename}")
            
            # Update database for plants that should use this image
            scientific_name = correct_filename.replace('.jpg', '').replace('_', ' ').title()
            c.execute("UPDATE plants SET image_url = ? WHERE scientific_name LIKE ?", 
                     (f"/static/images/{correct_filename}", f"%{scientific_name}%"))
        else:
            print(f"⚠️  File not found: {current_filename}")
    
    conn.commit()
    conn.close()
    print("Fixes completed!")

if __name__ == "__main__":
    fix_specific_matches()
