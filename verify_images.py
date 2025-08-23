import sqlite3

def verify_image_updates():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    
    # Get all plants with their updated image URLs
    c.execute("SELECT id, scientific_name, image_url FROM plants")
    plants = c.fetchall()
    
    print("Updated plant image paths:")
    print("ID | Scientific Name | Image URL")
    print("-" * 80)
    
    local_images = 0
    external_urls = 0
    
    for plant in plants:
        plant_id, scientific_name, image_url = plant
        status = "✅ LOCAL" if image_url.startswith('/static/images/') else "🌐 EXTERNAL"
        print(f"{plant_id:2} | {scientific_name:30} | {image_url} {status}")
        
        if image_url.startswith('/static/images/'):
            local_images += 1
        else:
            external_urls += 1
    
    print(f"\nSummary:")
    print(f"Local images: {local_images}")
    print(f"External URLs: {external_urls}")
    print(f"Total plants: {local_images + external_urls}")
    
    conn.close()

if __name__ == "__main__":
    verify_image_updates()
