"""
CropGuard AI - Plant Disease Treatment & Recommendation Module
Provides structured recommendations (Organic, Chemical, Prevention) based on diagnosed plant diseases.
"""

DISEASE_RECOMMENDATIONS = {
    "Apple___Apple_scab": {
        "disease_name": "Apple Scab",
        "crop": "Apple",
        "description": "Fungal infection caused by Venturia inaequalis leading to dark, velvety olive-green spots on leaves and fruit.",
        "organic_control": [
            "Apply neem oil or sulfur spray early in the growing season.",
            "Rake and destroy fallen leaves in autumn to reduce overwintering spores.",
            "Prune trees to improve air circulation and sunlight penetration."
        ],
        "chemical_control": [
            "Fungicides containing Myclobutanil, Captan, or Mancozeb.",
            "Apply at green tip stage and repeat according to label instructions during wet weather."
        ],
        "preventive_measures": [
            "Plant scab-resistant apple cultivars (e.g., Liberty, Enterprise, Freedom).",
            "Avoid overhead irrigation to keep foliage dry."
        ],
        "soil_irrigation_advice": "Ensure well-drained soil with a pH of 6.0 to 7.0. Drip irrigation is recommended."
    },
    "Apple___Black_rot": {
        "disease_name": "Apple Black Rot",
        "crop": "Apple",
        "description": "Caused by the fungus Botryosphaeria obtusa, causing leaf spots ('frogeye'), cankers on branches, and fruit rot.",
        "organic_control": [
            "Prune out dead or diseased wood and mummified fruit during winter dormant pruning.",
            "Apply copper-based sprays prior to leaf emergence."
        ],
        "chemical_control": [
            "Fungicides containing Thiophanate-methyl, Captan, or Fludioxonil."
        ],
        "preventive_measures": [
            "Keep trees vigorous with balanced fertilization.",
            "Remove dead twigs and mummified fruits from surrounding areas."
        ],
        "soil_irrigation_advice": "Avoid excess nitrogen fertilizer which creates dense foliage conducive to fungal growth."
    },
    "Apple___healthy": {
        "disease_name": "Healthy Apple Tree",
        "crop": "Apple",
        "description": "The apple foliage appears healthy with no visible signs of pathogen infection.",
        "organic_control": [
            "Maintain current organic practices.",
            "Apply compost tea occasionally to boost leaf immunity."
        ],
        "chemical_control": [
            "No chemical intervention needed."
        ],
        "preventive_measures": [
            "Monitor regularly for early signs of pests or fungal spots.",
            "Maintain balanced pruning and orchard hygiene."
        ],
        "soil_irrigation_advice": "Maintain soil moisture with organic mulch layer."
    },
    "Corn_(maize)___Common_rust_": {
        "disease_name": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "description": "Fungal disease caused by Puccinia sorghi, causing reddish-brown powdery pustules on leaves.",
        "organic_control": [
            "Spray with potassium bicarbonate or copper fungicides if infection is early and severe.",
            "Apply compost tea to enhance plant vigor."
        ],
        "chemical_control": [
            "Fungicides containing Azoxystrobin, Pyraclostrobin, or Propiconazole."
        ],
        "preventive_measures": [
            "Plant rust-resistant corn hybrids.",
            "Practice crop rotation with non-cereal crops."
        ],
        "soil_irrigation_advice": "Ensure adequate potassium levels in soil to improve disease tolerance."
    },
    "Corn_(maize)___healthy": {
        "disease_name": "Healthy Corn Plant",
        "crop": "Corn (Maize)",
        "description": "The corn leaves show deep green coloration and no pustules or blights.",
        "organic_control": [
            "Maintain routine organic soil conditioning."
        ],
        "chemical_control": [
            "No treatment required."
        ],
        "preventive_measures": [
            "Ensure proper crop spacing for good air movement.",
            "Rotate crops annually."
        ],
        "soil_irrigation_advice": "Maintain uniform moisture during critical tasseling and silking stages."
    },
    "Potato___Early_blight": {
        "disease_name": "Potato Early Blight",
        "crop": "Potato",
        "description": "Caused by Alternaria solani, characterized by dark brown spots with concentric rings ('target board' pattern) on older leaves.",
        "organic_control": [
            "Apply copper octanoate or bio-fungicides based on Bacillus subtilis.",
            "Remove lower infected leaves to reduce spore spread."
        ],
        "chemical_control": [
            "Fungicides containing Chlorothalonil, Mancozeb, or Difenoconazole."
        ],
        "preventive_measures": [
            "Practice 3 to 4 year crop rotation with non-solanaceous crops.",
            "Use certified disease-free seed potatoes."
        ],
        "soil_irrigation_advice": "Avoid furrow or overhead watering; prefer drip irrigation to keep foliage dry."
    },
    "Potato___Late_blight": {
        "disease_name": "Potato Late Blight",
        "crop": "Potato",
        "description": "Devastating disease caused by Phytophthora infestans, causing water-soaked dark lesions with white mold on leaf undersides.",
        "organic_control": [
            "Apply fixed copper fungicides immediately upon first detection.",
            "Destroy infected vines prior to harvest to prevent tuber infection."
        ],
        "chemical_control": [
            "Systemic fungicides containing Metalaxyl, Cymoxanil, or Mandipropamid."
        ],
        "preventive_measures": [
            "Destroy volunteer potato plants and nightshade weeds.",
            "Plant resistant varieties like Sarpo Mira or Defender."
        ],
        "soil_irrigation_advice": "Ensure high hilling of tubers to protect them from spores washing down through soil."
    },
    "Potato___healthy": {
        "disease_name": "Healthy Potato Plant",
        "crop": "Potato",
        "description": "Vigorous potato foliage with no signs of blights or viral mottling.",
        "organic_control": [
            "Continue standard organic monitoring."
        ],
        "chemical_control": [
            "No chemical treatment needed."
        ],
        "preventive_measures": [
            "Keep field weed-free.",
            "Maintain proper hilling around plants."
        ],
        "soil_irrigation_advice": "Keep soil evenly moist, avoid waterlogging."
    },
    "Tomato___Bacterial_spot": {
        "disease_name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "description": "Caused by Xanthomonas bacteria, resulting in small, dark, water-soaked spots on leaves and fruit with yellow halos.",
        "organic_control": [
            "Apply copper sprays combined with Mancozeb or organic copper formulations.",
            "Remove infected foliage early."
        ],
        "chemical_control": [
            "Copper hydroxide combined with streptomycin or copper bactericides."
        ],
        "preventive_measures": [
            "Use pathogen-free certified seeds.",
            "Sanitize garden tools, stakes, and cages between seasons."
        ],
        "soil_irrigation_advice": "Mulch generously around base to prevent soil splashing onto lower leaves."
    },
    "Tomato___Early_blight": {
        "disease_name": "Tomato Early Blight",
        "crop": "Tomato",
        "description": "Caused by Alternaria linariae, producing dark spots with concentric rings on lower leaves first.",
        "organic_control": [
            "Apply bio-fungicides containing Bacillus amyloliquefaciens or neem oil.",
            "Prune off lower leaves up to 12 inches from the ground."
        ],
        "chemical_control": [
            "Chlorothalonil, Mancozeb, or Copper-based fungicides."
        ],
        "preventive_measures": [
            "Stake and cage tomato plants to keep leaves elevated.",
            "Apply straw mulch to prevent soil-borne spore splash."
        ],
        "soil_irrigation_advice": "Water strictly at soil level early in the morning."
    },
    "Tomato___Late_blight": {
        "disease_name": "Tomato Late Blight",
        "crop": "Tomato",
        "description": "Severe infection by Phytophthora infestans, causing pale green to brown water-soaked lesions that spread rapidly in humid weather.",
        "organic_control": [
            "Apply copper fungicides as a preventive measure before rain events.",
            "Remove and bag infected plants completely."
        ],
        "chemical_control": [
            "Fungicides containing Dimethomorph, Propamocarb, or Chlorothalonil."
        ],
        "preventive_measures": [
            "Do not plant tomatoes near potatoes.",
            "Provide maximum spacing between plants for ventilation."
        ],
        "soil_irrigation_advice": "Ensure excellent soil drainage and avoid overhead watering."
    },
    "Tomato___healthy": {
        "disease_name": "Healthy Tomato Plant",
        "crop": "Tomato",
        "description": "Leaves are vibrant green, stem is sturdy, and flowers/fruit show no lesions.",
        "organic_control": [
            "Apply organic compost or fish emulsion periodically."
        ],
        "chemical_control": [
            "No chemical action required."
        ],
        "preventive_measures": [
            "Stake plants early and prune suckers to optimize airflow."
        ],
        "soil_irrigation_advice": "Maintain deep, infrequent watering at the root zone."
    }
}

DEFAULT_RECOMMENDATION = {
    "disease_name": "Unspecified Plant Disease / Condition",
    "crop": "General Crop",
    "description": "Pathogen details not specifically indexed in local offline database.",
    "organic_control": [
        "Isolate affected foliage and prune visibly damaged tissues.",
        "Apply broad-spectrum organic neem oil spray or horticultural soap.",
        "Ensure daytime sunlight exposure and adequate spacing."
    ],
    "chemical_control": [
        "Consult a local agricultural extension office or agronomist for targeted treatment options."
    ],
    "preventive_measures": [
        "Practice crop rotation.",
        "Sanitize pruning shears between plants.",
        "Avoid foliage wetting during irrigation."
    ],
    "soil_irrigation_advice": "Maintain balanced soil fertility and ensure proper drainage."
}

def get_recommendations(disease_key: str) -> dict:
    """
    Retrieve treatment and preventive recommendations for a given disease class key.
    """
    return DISEASE_RECOMMENDATIONS.get(disease_key, DEFAULT_RECOMMENDATION)
