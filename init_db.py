import sqlite3

def create_and_seed_db():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()

    # Drop table if exists
    c.execute('DROP TABLE IF EXISTS plants')

    # Create plants table
    c.execute('''
        CREATE TABLE plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scientific_name TEXT NOT NULL,
            common_name TEXT,
            flowering_time TEXT,
            height TEXT,
            growing_requirements TEXT
        )
    ''')

    # Plant data to insert
    plants_data = [
        ("Acacia acinacea", "Gold Dust Wattle", "Sept-Dec", "0.5–2 m", "Full sun to part shade; well-drained soils (sandy, loam, gravel); drought- and frost-tolerant; low maintenance; light pruning beneficial (Newport Nursery, map.whitehorse.vic.gov.au, anbg.gov.au, Australian Plants Society | Resources)"),
        ("Acacia dealbata", "Silver Wattle", "Jun-Oct", "15–30 m", "Full sun; well-drained soils; fast-growing; good for shade and screening (bindy.com.au)"),
        ("Acacia implexa", "Lightwood", "Dec-Mar", "~5–15 m", "Well-drained sandy or clay soils; full sun; drought-tolerant; used for timber/rope (Gardening Channel, bindy.com.au)"),
        ("Acacia mearnsii", "Black Wattle", "Sept-Nov", "~5–15 m", "Full sun; moist, well-drained soils; attracts wildlife; used for tannin (bindy.com.au, Wikipedia)"),
        ("Acacia melanoxylon", "Blackwood", "Jul-Oct", "~15–30 m", "Full sun; fertile, well-drained soils; high rainfall; valued timber (bindy.com.au, Wikipedia)"),
        ("Acacia montana", "Mallee Wattle", "Sept-Dec", "~1–2 m", "Well-drained soils; full sun; compact shrub for small gardens (Newport Nursery)"),
        ("Acacia paradoxa", "Kangaroo Thorn", "Aug-Dec", "~1–3 m", "Full sun; well-drained soils; prickly, wildlife-friendly (Newport Nursery)"),
        ("Acacia provincialis", "Swamp Wattle", "Dec-Feb", "~2–4 m", "Moist, well-drained soils; full sun; suitable for wetland areas (Newport Nursery)"),
        ("Acacia pycnantha", "Golden Wattle", "Jun-Nov", "~4–8 m", "Full sun; wide soil tolerance; drought-resistant; windbreak; mild salinity (Wikipedia)"),
        ("Acacia rostriformis", "Rostriform Wattle", "Aug-Nov", "~2–4 m", "Likely similar to other wattles: full sun; well-drained soils (Newport Nursery)"),
        ("Acaena echinata", "Sheep's Burr", "Aug-Nov", "~0.3–0.5 m", "Well-drained soils; full sun to part shade; low maintenance groundcover (Newport Nursery)"),
        ("Acaena novae-zealandiae", "Bidgee Widgee", "Sept-Dec", "~0.2–0.3 m", "Well-drained soils; full sun; mat-forming groundcover; low maintenance (Newport Nursery)"),
        ("Alisma plantago-aquatica", "Water Plantain", "Jun-Aug", "~0.5–1 m", "Moist or aquatic soils; full sun; suitable for ponds/wet areas (Newport Nursery)"),
        ("Allocasuarina leuhmannii", "Buloke", "All months", "~5–10 m", "Full sun; well-drained sandy soils; habitat tree; drought-tolerant (Newport Nursery)"),
        ("Allocasuarina verticillata", "Drooping Sheoke", "Mar-Dec", "~3–6 m", "Full sun; sandy, well-drained soils; timber use; restoration plant (Newport Nursery)"),
        ("Amphibromus neesii", "Swamp Wallaby Grass", "Oct-Apr", "~0.5–1 m", "Moist, well-drained soils; full sun; suitable for wet areas (Newport Nursery)"),
        ("Amphibromus nervosus", "Common Swamp Wallaby", "Oct-Jan", "~0.5–1 m", "Moist, well-drained soils; full sun; wetland grass (Newport Nursery)"),
        ("Triglochin Striata", "Arrowgrass", "May-Aug", "~0.3–0.5 m", "Moist soils; full sun; aquatic marginal plant (Newport Nursery)"),
        ("Arthropodium fimbriatum", "Nodding Chocolate Lily", "Sept-Nov", "~0.8 m", "Well-drained soils; full sun; fragrant flowers; low maintenance (Newport Nursery) Located on moderately moist to dry sites. Climatic zones can vary from less than 18 inches of annual precipitation up to 60 inches in wetter climatic zone"),
        ("Arthropodium minus", "Small Vanilla Lily", "Aug-Dec", "~0.3–1 m", "Well-drained soils in full sun or semi-shade. Often shallow rocky soils. Can tolerate dry conditions."),
        ("Arthropodium strictum", "Chocolate Lily", "Jan-Mar", "Up to 0.6 m", "Well-drained soils; full sun; star-shaped flowers (Newport Nursery)"),
        ("Asperula conferta", "Common Woodruff", "Sept-Dec", "~0.15-0.3m", "Well-drained soils; full sun; aromatic groundcover (Newport Nursery) Usually grows in moist, well-drained soils."),
        ("Atriplex cinerea", "Coastal Saltbush", "Oct-Feb", "~1–2 m (height) 1-2m (width)", "Full/partial shade, sandy/loamy/saline soils, shrub type. Minimal maintenance is required, a light prune after flowering will encourage new growth and keep the plant looking healthy.Well drained soil and full sunny position. Attracts Birds. Atriplex Cinerea thrives in coastal environments. It is able to colonising sand dunes despite the prevailing winds and sea spray."),
        ("Atriplex paludosa", "Marsh Saltbush", "Oct-Apr", "1-1.15m (h) 1-2m (w)", "Clay/loam/sandy soils - Full/partial shade conditions - Saltmarsh environments - Highlight tolerant to saline conditions (for coastal areas)."),
        ("Atriplex suberecta", "Lagoon Saltbush", "May-Jul", "1m", "Well-drained loam/sandy soils; full sun; tolerant of drought, salinity, frost; low maintenance It can grow in full sun or semi shade and in clay soil. Saltbush is a small bush used as fodder for livestock. Reduced demand for irrigation water. Plants are less stressed."),
        ("Suaeda australis", "Austral Seablite", "Oct-Mar", "~0.2–0.8 m tall, spreads to ~2 m", "Moist sandy/clay soils; full sun to semi-shade; highly salt- and wind-tolerant; low maintenance (PFAF, australianecosystems.com.au)"),
        ("Atriplex semibaccata", "Australian saltbush", "Nov-Mar", "1m", "It can grow in basalt soil. Requires semi-shade to full sun for growth."),
        ("Austrostipa bigeniculata", "Tall Spear-Grass", "Jan, Nov, Dec", "~0.5–1.2 m", "Heavy clay/alluvial soils; full sun; drought-tolerant; moderate maintenance; attracts birds -The stems disintegrate after the seedheads develop. Seeds are covered in short whitish hairs and a hairy bristle or awn that is up to 40 mm long, kinked twice. A food source for seed-eating birds, including finches. It also attracts moths and butterflies."),
        ("Austrostipa breviglumis", "Cane Spear Grass", "Sep–Dec", "~1.6 m", "Skeletal soils in drier areas; full sun; drought-tolerant; low maintenance (Newport Nursery)"),
        ("Austrostipa elegantissima", "Feather Spear Grass", "Sep–Nov", "~0.12 m", "Varied soils (granite, sand, saline flats); full sun; adaptable, low maintenance (Newport Nursery, Nurseries Online Australia) -Occurs on a variety of substrates including granitic, shaly or calcareous cliffs, limestone-rich mallee soils, deep sand and saline flats, and Quaternary basalt derived soils, mostly in areas of low effective rainfall."),
        ("Austrostipa gibbosa", "Spear-grass", "Oct-Jan", "~1.5 m", "Heavy alluvial/basalt soils; full sun; uncommon; low maintenance, habitat grass (Newport Nursery)"),
        ("Austrostipa mollis", "Soft Spear Grass", "Sept-Dec", "~0.6m", "Moist to dry forests; full sun to semi-shade; frost/snow tolerant; moderate maintenance. - Uncommon, mostly confined to heavy alluvial or basalt-derived soils. The floret of this species is gibbous, with an eccentric awn. -Soil adaptable, Dry Sclerophyll Forest "),
        ("Austrostipa scabra ssp. falcata", "Slender Spear Grass", "All year", "~0.6 m", "Clay-adaptable; full sun; drought-tolerant; low maintenance (Newport Nursery, Nurseries Online Australia)"),
        ("Austrostipa semibarbata", "Fibrous Speargrass", "Sept-Dec", "~0.3 m", "Dry soils in woodland and grassland. Frost tolerant. Full sun, semi-shade. Drift through trees or use as accent plants in garden beds."),
        ("Austrostipa setacea", "Corkscrew Grass", "All year", "~1 m", "Full sun; well-drained soils; good for low maintenance gardens (Nurseries Online Australia) Collect when hard, dark seeds part from heads easily. Monitor closely as mature seeds quickly shed."),
        ("Austrostipa stipoides", "Coast spear grass", "Sept-Feb", "0.7m", "Likely similar to other wallaby/grass – full sun; well-drained; low maintenance Green in All seasons, Germination is slow and erratic. Sow seed in autumn with temperatures below 25C. Germination rates are improved with smoke treatment. Cut to the base in spring."),
        ("Banksia integrifolia", "Coastal Banksia", "Feb-Sept", "~10-15m", "Sandy, well-drained soils; full sun; coastal tolerant; moderate water; low maintenance Sandy loam, Clay loam, Saline, Poor soil Plant. Low maintenance garden, Flower garden, Coastal garden, Drought resistant."),
        ("Banksia marginata", "Silver Banksia", "Feb–July", "~3–6 m", " Does not tolerate waterlogging or high phosphorus fertilisers. A native fertiliser is recommended. A full sun position is preferred but part shade is tolerated."),
        ("Baumea articula", "Jointed Twig Rush", "Nov-Apr", "~0.9-2m", "Wet soils in swamps or in lagoons or slow-moving watercourses. Full sun, semi shade."),
        ("Sarcocornia Quinqueflora", "Bead Weed", "Mar-Jun", "~0.3m", "It can grow mostly in coastal areas and frequently in habitats periodically inundated by salt water."),
        ("Bossiaea prostrata", "Creeping Bossiaea", "Oct-Dec", "0.5m", "Able to grow in saline soils and establish on disturbed soil. - Full sun-Full shade - Well-drained soils - Benefits from some dappled shade in afternoon in hot climates - Groundcover purpose"),
        ("Bothriochloa", "Red-leg grass", "Dec-Apr", "0.02m", "- Drought tolerant - Attracts wildlife -Low shrubs - Loams and clays Not a wetland plant."),
        ("Brachyscome basaltica var.", "Basalt Daisy", "Sept-Jan", "0.5-0.6m", "- Grows in swampy ground, and drought sensitive."),
        ("Brachyscome dentata", "Lobe-seed Daisy", "Sept-Dec", "0.5m", " Hardy species that can survive in wet well-drained soil during winter and dry soil in summer."),
        ("Brachyscome multifida", "Cut-leaf Daisy (B.Ranges)", "Sept-Mar", "0.1-0.4m", "Moist well-drained clays and shallow rocky soils in forest areas. Full sun, dappled, and semi-shade."),
        ("Bulbine bulbosa", "Bulbine Lily", "Sept-Dec", "0.6-1m", "- Full sun to part shade -  Well-drained soils preference but tolerant to loamy, sandy loam and clay loam. - Regular watering. - Pest control. - Aesthetic purpose"),
        ("Bulbine glauca", "Rock Lily", "Sept-Feb", "0.6-1.8m", "Well-drained, adaptable to various soil types, including clay and seasonally inundated soils. Prefers moist conditions but can tolerate some dryness once established Full sun to part shade Tolerates light frost"),
        ("Bulbine semibarbata", "Leek Lily", "Sept-Feb", "0.3-0.5m", "Sunlight: Leek lilies prefer full sun or dappled shade, needing at least six hours of sunlight for optimal flowering according to PictureThis. Watering: They are drought-tolerant once established, but regular watering is needed, especially during dry weather. Allow the soil to dry out between waterings to prevent root rot according to PictureThis. Soil: Leek lilies prefer well-drained soil enriched with organic matter. They can tolerate a variety of soils, but good drainage is essential. Purpose: Leek lilies are used for both culinary and ornamental purposes. Their edible seeds, roots, and corms can be consumed. They are also attractive additions to rockeries, cottage gardens, and containers."),
        ("Bursaria spinosa var. spinosa", "Sweet Bursaria", "Oct-Mar", "3–6 m", "Full sun to partial shade; well-drained dry to moist soils; drought-tolerant; low maintenance; wildlife habitat"),
        ("Caesia calliantha", "Blue Grass-lily", "Sept-Jan", "0.7 m", "Well-drained sandy/clay/loam; full sun to partial shade; moderate water; moderate maintenance"),
        ("Calandrinia calyptrata", "Pink Purslane", "Aug-Dec", "0.01-0.05m", "Well-drained rocky soils; full sun; low maintenance (inferred succulent groundcover) Sandy soils over laterite, granite, or limestone"),
        ("Callistemon sieberi", "River Bottlebrush", "Nov-Mar", "2.5m", "Full sun; well-drained soil; moderate water; bird-attracting (typical callistemon traits) This plant is not fussy about soil texture, structure or pH. It prefers a moist soil, but will tolerate dry conditions."),
        ("Callitris glaucophylla", "White Cypress Pine", "Oct-Feb", "5-12 m", "Well-drained soils; full sun; drought-tolerant; low maintenance Low maintenance garden, Courtyard, Poolside, Coastal garden, Drought resistant. Sunny, Light shade. Dry, Well-drained."),
        ("Calocephalus citreus", "Lemon Beauty Heads", "Dec-Mar", "~0.6 m", "Well-drained soil; full sun; low water; groundcover Well-drained sites in grasslands and woodlands. Hardy, drought-resistant plant and salt tolerant."),
        ("Calocephalus lacteus", "Milky Beauty Heads", "Dec-Mar", "~0.05-0.7m", "Full sun, well-drained soil. May require additional water during long dry periods, frost tolerant."),
        ("Calotis scabiosifolia", "Rough Burr Daisy", "May-Oct", "~0.45m", "Dry well-drained soils of foothills. Full sun, semi-shade."),
        ("Calotis scapigera", "Tufted Burr Daisy", "Oct-Mar", "~0.35-0.4 m", "Well-drained soil; full sun"),
        ("Carex appressa", "Tall Sedge", "Aug-Jan", "0.8-1m", "Moist to wet soil; full sun to partial shade; tolerates temporary inundation; low maintenance; erosion control; wildlife habitat (wsbn.org.au, australianplantsonline.com.au)"),
        ("Carex bichenoviana", "Plains Sedge", "Oct-Feb", "~0.25-0.5", "Wet soils; sun to partial shade; wetland suitable"),
        ("Carex fascicularis", "Tassel Sedge", "Oct-Apr", "~0.6-1.5", "Wet soils; sun to partial shade; wetland plant"),
        ("Carex incomitata", "Razor  Sedge", "Mar-Sept", "2.5m", "Grow in either Sun or shade. Cool zones should plant in Sun while warmer locations will find better production if the plants are situated in slightly shady parts of the garden."),
        ("Carex inversa", "Knob Sedge", "Sept-Apr", "0.3-0.75m", "• Soil: Moist, well-drained soils are ideal, but it can also tolerate seasonally dry conditions. • Sunlight: It thrives in full sun to partial shade. • Watering: Consistent moisture is important, especially during dry periods. It can tolerate occasional inundation, but prefers not to be waterlogged"),
        ("Carex tasmanica", "Mr Curly Sedge", "Sept-Nov", "~0.2 m", "Sunlight: Curly sedge can tolerate full sun, but also thrives in partial shade. Soil: It prefers heavy, clay soils, and can tolerate saline conditions. The soil should be seasonally moist or waterlogged. Watering: Curly sedge needs regular watering, especially when young, and can tolerate some waterloggin"),
        ("Carex tereticaulis", "Common Sedge", "Sept-Oct", "0.7–1 m (Wikipedia)", "Clay/alluvial soils; seasonally inundated wetlands; low maintenance"),
        ("Carpobrotus modestus", "Inland Pigface", "Aug-Nov", "0.2–0.3 m tall, spreads 1–2 m", "Sandy/coastal soils; full sun; salt- and drought-tolerant; low maintenance"),
        ("Carpobrotus rossii", "Ross’ Noonflower", "Mar-Nov", "0.2-0.4m", "light (sandy), medium (loamy), and heavy (clay) soils and prefers well-drained soil. It can grow in semi-shade or no shade."),
        ("Cassinia longifolia", "Shiny Cassinia", "Nov-Mar", "1.2–2.5m H & 1.0–1.5 m W", "Full sun; well")
    ]

    # Insert plant data
    c.executemany('''
        INSERT INTO plants (scientific_name, common_name, flowering_time, height, growing_requirements)
        VALUES (?, ?, ?, ?, ?)
    ''', plants_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_and_seed_db()
    print("Database created and seeded successfully.")
