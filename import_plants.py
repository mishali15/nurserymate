import sqlite3
import re

def parse_plant_data(text_data):
    """Parse the plant data from the provided text format"""
    plants = []
    lines = text_data.strip().split('\n')
    
    # Skip the header line
    for line in lines[1:]:
        if not line.strip():
            continue
            
        # Split by tabs (assuming tab-separated values)
        parts = line.split('\t')
        if len(parts) >= 12:
            plant = {
                'scientific_name': parts[0].strip(),
                'common_name': parts[1].strip(),
                'flowering_time': parts[2].strip(),
                'height': parts[3].strip(),
                'ecological_function': parts[4].strip(),
                'sunlight': parts[5].strip(),
                'water_level': parts[6].strip(),
                'salt_wind_tolerance': parts[7].strip(),
                'type': parts[8].strip(),
                'planting_space': parts[9].strip(),
                'image_url': parts[10].strip(),
                'soil_type': parts[11].strip()
            }
            
            plants.append(plant)
    
    return plants

def import_plants_to_db(plants):
    """Import plants into the SQLite database"""
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    
    # Ensure the table exists with the correct schema
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
    
    # Insert plants
    for plant in plants:
        c.execute('''
            INSERT INTO plants (
                scientific_name, common_name, flowering_time, height,
                ecological_function, sunlight, water_level, salt_wind_tolerance,
                type, planting_space, image_url, soil_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            plant['scientific_name'],
            plant['common_name'],
            plant['flowering_time'],
            plant['height'],
            plant['ecological_function'],
            plant['sunlight'],
            plant['water_level'],
            plant['salt_wind_tolerance'],
            plant['type'],
            plant['planting_space'],
            plant['image_url'],
            plant['soil_type']
        ))
    
    conn.commit()
    conn.close()
    print(f"Successfully imported {len(plants)} plants into the database!")

def main():
    # Your plant data goes here (copy-paste the entire table)
    plant_data = """Scientific name	Common name 	Flowering time 	Height	Ecological function 	Sunlight	Water level	Salt/wind tolerance	Type	Planting space	Image address	Soil type 
Acacia acinacea	Gold Dust Wattle	Sept-Dec	0.5–2 m	Attracts birds/butterflies	Full sun	Moderate	No	Shrub	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Acacia-acinacea.jpg	Moist/well-drained, loamy, clay
Acacia dealbata	Silver Wattle	Jun-Oct	15–30 m	Structural/visual interest/Attracts birds/butterflies	Full sun	Moderate	No	Tree	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Acacia_dealbata-1-2-300x300.jpg	Moist/well-drained, loamy, sandy
Acacia implexa	Lightwood	Dec-Mar	~5–15 m	Structural/visual interest/Attracts birds/butterflies/low maintenance	Full sun / partial shade	Moderate	No	Tree	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Acacia_implexa_flowers_1-300x300.jpg	Moist/well-drained, clay, loamy
Acacia mearnsii	Black Wattle	Sept-Nov	~5–15 m	Structural/visual interest	Full sun	Moderate	No	Tree	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Acacia_mearnsii_blossoms-300x300.jpg	Heavy/clay, moist/well-drained
Acacia melanoxylon	Blackwood	Jul-Oct	~15–30 m	Visual/ attracts animals/low maintenance	Full sun / partial shade	Moderate	No	Tree	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/07/1024px-Acacia_melanoxylon-300x300.jpg	Moist/well-drained, clay, loamy
Acacia montana	Mallee Wattle	Sept-Dec	~1–2 m	Low maintenance/attracts birds	Full sun	Dry–moderate	No	Shrub	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Mallee-Wattle-300x300.jpg	Dry/sandy/loamy, clay
Acacia paradoxa	Kangaroo Thorn	Aug-Dec	~1–3 m	Structural/visual	Full sun	Dry–moderate	No	Shrub	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Hedge-Wattle-300x300.jpg	Dry/sandy/loamy, tolerates poor soils
Acacia provincialis	Swamp Wattle	Dec-Feb	~2–4 m	Attracts birds/low maintenance	Full sun / partial shade	Wet–moderate	No	Shrub	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Acacia_provincialis_Wirilda._24972617986-300x300.jpg	Moist/well-drained, clay loam
Acacia pycnantha	Golden Wattle	Jun-Nov	~4–8 m	Visual/ attracts animals/low maintenance	Full sun	Dry–moderate	No	Shrub	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Golden-Wattle-300x300.jpg	Dry/sandy/loamy, well-drained
Acacia rostriformis	Rostriform Wattle	Aug-Nov	~2–4 m	Structural/visual interest/Attracts birds/butterflies	Full sun	Moderate	No	Shrub	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Varnish-Wattle-300x300.jpg	Moist/well-drained, loamy, sandy
Acaena echinata	Sheep's Burr	Aug-Nov	~0.3–0.5 m	Provides food, attracts insects, low maintenance	Full sun / partial shade	Dry–moderate	No	Groundcover	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Acaena-echinata-300x300.jpg	Moist/well-drained, clay loam
Acaena novae-zealandiae	Bidgee Widgee	Sept-Dec	~0.2–0.3 m	Structural/provides seeds/attracts small birds	Full sun / partial shade	Moderate	Yes (coastal or external site)	Groundcover/creeping	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Bidgee-Widgee-300x300.jpg	Moist/well-drained, loamy, sandy
Alisma plantago-aquatica	Water Plantain	Jun-Aug	~0.5–1 m	Attracts butterfiles/insects, structural interest	Full sun	Wet/swampy	No	Small herb	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/02/Alisma-plantago-aquatica-300x300.jpg	Heavy/clay/waterlogged, swampy soils
Allocasuarina leuhmannii	Buloke	All months	~5–10 m	Attracts birds, structural/visual interest	Full sun	Dry–moderate	No	Tree	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Buloke-1-300x300.jpg	Dry/sandy/loamy, well-drained
Allocasuarina verticillata	Drooping Sheoke	Mar-Dec	~3–6 m	Attracts birds, structural/visual interest	Full sun	Dry–moderate	Yes (coastal or external site)	Tree	Medium	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Drooping-Sheoke-300x300.jpg	Dry/sandy/loamy, coastal sandy soils
Amphibromus neesii	Swamp Wallaby Grass	Oct-Apr	~0.5–1 m	Attracts birds, low maintenance	Full sun	Wet–moderate	No	Tufting/grass-like	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Swamp-Wallaby-Grass-300x300.jpg	Heavy/clay, seasonal wet areas
Amphibromus nervosus	Common Swamp Wallaby	Oct-Jan	~0.5–1 m	Low maintenance/structural	Full sun	Wet–moderate	No	Tufting/grass-like	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Common-Swamp-Wallaby-Grass-300x300.jpg	Heavy/clay, waterlogged, wetland
Triglochin Striata	Arrowgrass	May-Aug	~0.3–0.5 m	Attracts butterfiles/insects, structural interest	Full sun	Wet/swampy	No	Tufting/grass-like	Low	https://newportnativenursery.com.au/wp-content/uploads/2023/06/14.-triglochin-striata-300x300.jpg	Heavy/clay/waterlogged, swampy
Arthropodium fimbriatum	Nodding Chocolate Lily	Sept-Nov	~0.8 m	Attracts butterfiles/insects, structural interest	Full sun / partial shade	Moderate	No	Small herb/dainty flower	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Arthropodium-fimbriatum-300x300.jpg	Moist/well-drained, loamy
Arthropodium minus	Small Vanilla Lily	Aug-Dec	~0.3–1 m	Provides food, attracts insects, visual	Full sun / partial shade	Moderate	No	Small herb/dainty flower	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Arthropodium-minus-300x300.jpg	Moist/well-drained, loamy, sandy
Arthropodium strictum	Chocolate Lily	Jan-Mar	Up to 0.6 m	Provides food, attracts insects, visual	Full sun / partial shade	Moderate	No	Small herb/dainty flower	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Arthropodium-strictum-300x300.jpg	Moist/well-drained, clay, loamy
Asperula conferta	Common Woodruff	Sept-Dec	~0.15-0.3m		Full sun / partial shade	Moderate	No	Small herb/dainty flower	Low	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Asperula-conferta-300x300.jpg	Dry/sandy/loamy, well-drained
Atriplex cinerea	Coastal Saltbush	Oct-Feb	~1–2 m (height) 1-2m (width)	Low maintenance, Visual/Structural interest, Provides food	Full sun	Dry–moderate	Yes (coastal)	Shrub	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Coastal-Saltbush-300x300.jpg	Saline/coastal, sandy
Atriplex paludosa	Marsh Saltbush	Oct-Apr	1-1.15m (h) 1-2m (w)	Low maintenance, Visual/Structural interest, Provides food	Full sun	Wet–moderate	Yes (coastal)	Shrub	Low	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Marsh-Saltbush-300x300.jpg	Saline/coastal, clay loam
Atriplex suberecta	Lagoon Saltbush	May-Jul	1m	Attracts birds, structural interest	Full sun	Wet/swampy	Yes-coastal	Groundcover/Creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Lagoon-Saltbush-300x300.jpg	Saline/coastal, loamy
Suaeda australis	Austral Seablite	Oct-Mar	~0.2–0.8 m tall, spreads to ~2 m 	Provides food, low maintenance	Full sun	Wet/swampy	Yes-coastal	Groundcover/Creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2023/06/12.-suaeda-australis-300x300.jpg	Saline/coastal, sandy loam
Atriplex semibaccata	Australian Saltbush	Nov-Mar	1m	Structural interest, low maintenance	Full sun	Dry/Drought prone	Yes-coastal	Groundcover/Creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2023/06/Atriplex-300x300.jpg	Saline/coastal, sandy
Austrostipa bigeniculata	Tall Spear-Grass	Jan, Nov, Dec	~0.5–1.2 m 	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Tall-Spear-grass-300x300.jpg	Dry/sandy/loamy, well-drained
Austrostipa breviglumis	Cane Spear Grass	Sep–Dec	1.6	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2023/06/1.-Austrostipa-breviglumis-300x300.jpg	Dry/sandy/loamy, rocky soils
Austrostipa elegantissima	Feather Spear Grass	Sep–Nov	~0.12 m (Newport Nursery, Nurseries Online Australia)	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Feather-Spear-Grass-300x300.jpg	Dry/sandy/loamy
Austrostipa gibbosa	Spear-grass	Oct-Jan	~1.5 m (Newport Nursery, Greg App)	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Spear-grass-300x300.jpg	Dry/sandy/loamy, rocky
Austrostipa mollis	Soft Spear Grass	Sept-Dec	~0.6m	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Soft-Spear-Grass-300x300.jpg	Dry/sandy/loamy
Austrostipa scabra ssp. falcata	Slender Spear Grass	All year	~0.6 m 	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Slender-spear-grass-300x300.png	Dry/sandy/loamy
Austrostipa semibarbata	Fibrous Speargrass	Sept-Dec	0.3m 	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Fibrous-Spear-Grass-300x300.jpg	Dry/sandy/loamy
Austrostipa setacea	Corkscrew Grass	All year 	1m	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Corkscrew-Grass-300x300.jpg	Dry/sandy/loamy
Austrostipa stipoides	Coast Spear Grass	Sept-Feb	0.7m 	Attracts birds, structural interest	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Coast-Spear-Grass-300x300.jpg	Saline/coastal, sandy loam
Banksia integrifolia	Coastal Banksia	Feb-Sept	~10-15m	Attracts birds, structural interest	Full sun	Moderate moisture	Yes-coastal	Shrub/Tree	Large area (>3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Coastal-Banksia-300x300.jpg	Saline/coastal, sandy loam, well-drained
Banksia marginata	Silver Banksia	Feb–July	~3–6 m	Provides food, low maintenance	Full sun	Moderate moisture	Yes-coastal	Shrub/Tree	Large area (>3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Silver-Banksia-300x300.png	Heavy/clay/waterlogged
Baumea articula	Jointed Twig Rush	Nov-Apr	~0.9-2m	Provides food, low maintenance	Full sun	Wet/swampy	Yes-coastal	Small herb/dainty flower	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2022/04/Baumea-articulata--300x300.jpg	Saline/coastal, tidal mudflats
Sarcocornia quinqueflora	Bead Weed	Mar-Jun	~0.3m	Attracts butterflies, low maintenance	Full sun	Wet/swampy	Yes-coastal	Groundcover/Creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2023/06/11.-salicornia-quinqueflora-300x300.jpg	Moist/well-drained, sandy loam
Bossiaea prostrata	Creeping Bossiaea	Oct-Dec	0.5m	Structural interest, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Groundcover/Creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Creeping-Bossiaea-300x300.jpg	Dry/sandy/loamy
Bothriochloa	Red-leg Grass	Dec-Apr	0.02m	Attracts butterflies, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Tufting/Grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Red-leg-Grass-300x300.jpg	Moist/well-drained, clay loam
Brachyscome basaltica var.	Basalt Daisy	Sept-Jan	0.5-0.6m	Attracts butterflies, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Brachyscome-basaltica-var.-300x300.jpg	Moist/well-drained, sandy loam
Brachyscome dentata	Lobe-seed Daisy	Sept-Dec	0.5m	Attracts butterflies, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Brachyscome-dentata-300x300.jpg	Moist/well-drained, clay loam
Brachyscome multifida	Cut-leaf Daisy	Sept-Mar	0.1-0.4m	Provides food, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Brachyscome-multifida-300x300.jpg	Moist/well-drained, sandy loam
Bulbine bulbosa	Bulbine Lily	Sept-Dec	0.6-1m	Provides food, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Bulbine-bulbosa-300x300.jpg	Moist/well-drained, sandy
Bulbine glauca	Rock Lily	Sept-Feb	0.6-1.8m	Provides food, low maintenance	Full sun	Dry/Drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Bulbine-glauca-300x300.jpg	Moist/well-drained, sandy loam
Bulbine semibarbata	Leek Lily	Sept-Feb	0.3-0.5m	Low maintenance, Visual/Structural interest, Provides food	Full sun	Dry/Drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Bulbine-semibarbata-300x300.jpg	Moist/well-drained, sandy loam
Bursaria spinosa var. spinosa	Sweet Bursaria 	Oct-Mar	3–6 m 	Attracts birds, provides food, low maintenance	Full sun	Moderate moisture	Yes-coastal	Shrub/tree	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Sweet-Bursaria-300x300.jpg	Moist/well-drained
Caesia calliantha	Blue Grass-lily	Sept-Jan	0.7 m 	Attracts butterflies, low maintenance	Full sun	Dry/drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Caesia-calliantha-300x300.jpg	Dry/sandy/loamy
Calandrinia calyptrata	Pink Purslane	Aug-Dec	0.01-0.05m	Attracts butterflies, low maintenance	Full sun	Dry/drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Calandrina-calyptrata-300x300.jpg	Dry/sandy/loamy
Callistemon sieberi	River Bottlebrush	Nov-Mar	2.5m	Attracts birds, low maintenance	Full sun	Moderate moisture	Yes-coastal	Shrub/tree	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/River-Bottlebrush-300x300.jpg	Moist/well-drained
Callitris glaucophylla	White Cypress Pine	Oct-Feb	5-12 m	Provides shelter, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Tree	Large area (>3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/08/Callitris-glaucophylla-300x300.png	Dry/sandy/loamy
Calocephalus citreus	Lemon Beauty Heads	Dec-Mar	~0.6 m	Provides food, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Calocephalus-citreus-300x300.jpg	Dry/sandy/loamy
Calocephalus lacteus	Milky Beauty Heads	Dec-Mar	~0.05-0.7m	Provides food, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Calocephalus-lacteus-300x300.jpg	Moist/well-drained
Calotis scabiosifolia	Rough Burr Daisy	May-Oct	~0.45m	Attracts butterflies, low maintenance	Full sun	Dry/drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Calotis-scabiosifolia-300x300.jpg	Dry/sandy/loamy
Calotis scapigera	Tufted Burr Daisy	Oct-Mar	~0.35-0.4 m	Attracts butterflies, low maintenance	Full sun	Dry/drought prone	No sheltered inland	Small herb/dainty flower	Small garden bed (<1m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Calotis-scapigera-300x300.jpg	Dry/sandy/loamy
Carex appressa	Tall Sedge	Aug-Jan	0.8-1m	Attracts birds, low maintenance	Full sun/partial	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Carex-appressa-300x300.jpg	Moist/well-drained
Carex bichenoviana	Plains Sedge	Oct-Feb	~0.25-0.5	Attracts birds, low maintenance	Full sun/partial	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Carex-Bichenoviana-300x300.jpg	Moist/well-drained
Carex fascicularis	Tassel Sedge	Oct-Apr	~0.6-1.5	Attracts birds, low maintenance	Full sun/partial	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2022/04/Carex-fascicularis-300x300.jpg	Moist/well-drained
Carex incomitata	Razor  Sedge	Mar-Sept	2.5m	Attracts birds, low maintenance	Full sun	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Carex-incomitata-300x300.jpg	Moist/well-drained
Carex inversa	Knob Sedge	Sept-Apr	0.3-0.75m	Attracts birds, low maintenance	Full sun/partial	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Carex-inversa-300x300.jpg	Moist/well-drained
Carex tasmanica	Mr Curly Sedge	Sept-Nov	~0.2 m	Attracts birds, low maintenance	Full sun/partial	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Carex-tasmanica-300x300.png	Moist/well-drained
Carex tereticaulis	Common Sedge	Sept-Oct	0.7-1m	Attracts birds, low maintenance	Full sun	Wet/swampy	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/12/Carex-tereticaulis-300x300.jpg	Moist/well-drained
Carpobrotus modestus	Inland Pigface	Aug-Nov	0.2–0.3 m tall, spreads 1–2 m 	Attracts birds, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Groundcover/creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Inland-Pigface-300x300.jpg	Saline/coastal
Carpobrotus rossii	Ross' Noonflower	Mar-Nov	0.2-0.4m	Attracts birds, low maintenance	Full sun/partial shade/no shade	Dry/drought prone	Yes-coastal	Groundcover/creeping	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2022/01/Ross-Noonflower-300x300.jpg	Saline/coastal
Cassinia longifolia	Shiny Cassinia	Nov-Mar	1.2–2.5m H & 1.0–1.5 m W	Attracts birds, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Shrub/tree	Large area (>3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Shiny-Cassinia-1-300x300.jpg	Dry/sandy/loamy
Cassinia arcuata	Chinese Scrub	Nov-Mar	~1–2 m	Attracts birds, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Shrub/tree	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/09/Chinese-Scrub-300x300.jpg	Dry/sandy/loamy
Chloris truncata	Windmill Grass	Nov-Jun	~0.1-0.5m	Attracts birds, low maintenance	Full sun	Dry/drought prone	Yes-coastal	Tufting/grass-like	Medium garden area (1–3m)	https://newportnativenursery.com.au/wp-content/uploads/2021/10/Windmill-Grass-300x300.jpg	Dry/sandy/loamy
"""
    
    # Parse and import the plants
    plants = parse_plant_data(plant_data)
    import_plants_to_db(plants)

if __name__ == "__main__":
    main()
