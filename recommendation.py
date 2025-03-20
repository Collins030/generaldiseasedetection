import streamlit as st
from PIL import Image


def get_recommendation(disease):
    recommendations = {
        "Apple___Apple_scab": {
            "disease_image": "assets/Apple___Apple_scab.jpg",
            "chemical": "Captan or Myclobutanil",
            "chemical_image": "assets/Captan.jpeg",
            "procedure": [
                "Apply Captan at the beginning of the growing season.",
                "Ensure thorough coverage on leaves and fruit.",
                "Reapply after heavy rainfall.",
                "Use resistant apple varieties when possible."
            ],
            "expected_outcome": "Apple trees with no scab infection and healthy fruit.",
            "healthy_image": "assets/apple_healthy.jpeg"
        },
        "Apple___Black_rot": {
            "disease_image": "assets/blackrot.jpeg",
            "chemical": "Thiophanate-methyl or Captan",
            "chemical_image": "assets/Captan.jpeg",
            "procedure": [
                "Prune infected branches and remove affected fruit.",
                "Apply fungicide during the growing season.",
                "Keep orchard clean and well-ventilated.",
                "Monitor trees regularly for signs of infection."
            ],
            "expected_outcome": "Healthy apple trees free from black rot.",
            "healthy_image": "assets/apple_healthy.jpeg"
        },
        "Apple___Cedar_apple_rust": {
            "disease_image": "assets/applecedar_rust.jpeg",
            "chemical": "Myclobutanil or Mancozeb",
            "chemical_image": "assets/Mancozeb.jpeg",
            "procedure": [
                "Apply fungicide early in the season.",
                "Remove nearby cedar trees if possible.",
                "Prune affected branches.",
                "Repeat treatment as per label instructions."
            ],
            "expected_outcome": "Apple trees with no rust infection.",
            "healthy_image": "assets/apple_healthy.jpeg"
        },
        "Apple___healthy": {
            "disease_image": "assets/apple_healthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical1.jpg",
            "procedure": [
                "Maintain proper watering and fertilization.",
                "Regularly inspect plants for signs of disease.",
                "Keep orchard clean and remove debris.",
                "Use disease-resistant varieties when planting."
            ],
            "expected_outcome": "Healthy apple trees with high yield.",
            "healthy_image": "assets/apple_healthy.jpeg"
        },
        "Potato___Late_blight": {
            "disease_image": "assets/potatolateblight.jpeg",
            "chemical": "Mancozeb or Metalaxyl",
            "chemical_image": "assets/Mancozeb.jpeg",
            "procedure": [
                "Mix the recommended dose of Mancozeb with water.",
                "Spray evenly on the affected leaves, ensuring full coverage.",
                "Repeat treatment every 7-10 days, especially in wet conditions.",
                "Monitor plant condition and remove heavily infected leaves."
            ],
            "expected_outcome": "Healthy potato crop with no signs of blight.",
            "healthy_image": "assets/potatohealthy.jpeg"
        },
        "Potato___healthy": {
            "disease_image": "assets/potatohealthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical1.jpg",
            "procedure": [
                "Plant certified disease-free seed potatoes.",
                "Implement proper crop rotation.",
                "Hill soil around plants as they grow.",
                "Provide consistent soil moisture."
            ],
            "expected_outcome": "Healthy potato plants with high tuber yield and quality.",
            "healthy_image": "assets/potatohealthy.jpeg"
        },
        "Potato___Early_blight": {
            "disease_image": "assets/potato_earlyblight.jpeg",
            "chemical": "Chlorothalonil or Azoxystrobin",
            "chemical_image": "assets/chlorothalonil.jpeg",
            "procedure": [
                "Apply fungicide at first sign of disease.",
                "Ensure thorough coverage of foliage.",
                "Remove lower infected leaves.",
                "Implement crop rotation with non-solanaceous crops."
            ],
            "expected_outcome": "Potato plants with minimal early blight damage and improved tuber yield.",
            "healthy_image": "assets/potatohealthy.jpeg"
        },
        "Blueberry___healthy": {
            "disease_image": "assets/bluberryhealthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical2.jpg",
            "procedure": [
                "Maintain well-drained soil.",
                "Provide adequate sunlight.",
                "Prune bushes regularly.",
                "Use organic mulch to retain moisture."
            ],
            "expected_outcome": "Healthy blueberry plants with high yield.",
            "healthy_image": "assets/bluberryhealthy.jpeg"
        },
        "Cherry_(including_sour)___Powdery_mildew": {
            "disease_image": "assets/Squash___Powdery_mildew.jpeg",
            "chemical": "Sulfur or Myclobutanil",
            "chemical_image": "assets/sulfur.jpeg",
            "procedure": [
                "Apply sulfur-based fungicide as soon as symptoms appear.",
                "Ensure good air circulation around trees.",
                "Prune affected branches.",
                "Repeat treatment as necessary."
            ],
            "expected_outcome": "Cherry trees free from powdery mildew.",
            "healthy_image": "assets/Powdery_mildew_chery.jpeg"
        },
        "Cherry_(including_sour)___healthy": {
            "disease_image": "assets/Squash___Powdery_mildew.jpeg",
            "chemical": "No chemical needed",
            "chemical_image": "added/chemical2.jpg",
            "procedure": [
                "Apply sulfur-based fungicide as soon as symptoms appear.",
                "Ensure good air circulation around trees.",
                "Prune affected branches.",
                "Repeat treatment as necessary."
            ],
            "expected_outcome": "Cherry trees free from powdery mildew.",
            "healthy_image": "assets/cherry_healthy.jpeg"
        },
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
            "disease_image": "assets/cercespora.jpeg",
            "chemical": "Strobilurin or Triazole-based fungicides",
            "chemical_image": "assets/Trizole.jpeg",
            "procedure": [
                "Apply fungicide at the early stages of infection.",
                "Rotate crops to prevent disease buildup.",
                "Maintain proper field sanitation and remove crop debris.",
                "Ensure adequate plant spacing for air circulation."
            ],
            "expected_outcome": "Corn plants with minimal to no leaf spot damage.",
            "healthy_image": "assets/maize_healthy.jpeg"
        },
        "Corn_(maize)___Common_rust_": {
            "disease_image": "assets/commonrust.jpeg",
            "chemical": "Propiconazole or Strobilurin-based fungicides",
            "chemical_image": "assets/propicanazole.jpeg",
            "procedure": [
                "Apply fungicide at the first signs of rust pustules.",
                "Plant rust-resistant corn varieties.",
                "Rotate crops to reduce pathogen buildup in the soil.",
                "Maintain optimal nitrogen levels to support plant health."
            ],
            "expected_outcome": "Corn plants free from rust, ensuring high yield.",
            "healthy_image": "assets/maize_healthy.jpeg"
        },
        "Corn_(maize)___Northern_Leaf_Blight": {
            "disease_image": "assets/Northernleafblight.jpeg",
            "chemical": "Azoxystrobin or Propiconazole",
            "chemical_image": "assets/propicanazole.jpeg",
            "procedure": [
                "Apply fungicide at early disease onset.",
                "Use resistant hybrids for planting.",
                "Practice crop rotation and remove infected residues.",
                "Ensure adequate plant spacing to improve airflow."
            ],
            "expected_outcome": "Corn plants with minimal leaf blight damage and healthy growth.",
            "healthy_image": "assets/maize_healthy.jpeg"
        },
        "Corn_(maize)___healthy": {
            "disease_image": "assets/maize_healthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical2.jpg",
            "procedure": [
                "Provide adequate nitrogen fertilization.",
                "Rotate crops yearly to maintain soil health.",
                "Monitor for pests and diseases regularly.",
                "Ensure proper irrigation and drainage to prevent root rot."
            ],
            "expected_outcome": "Healthy corn plants with maximum yield potential.",
            "healthy_image": "assets/maize_healthy.jpeg"
        },
        "Grape___Black_rot": {
            "disease_image": "assets/grapeblackrot.jpeg",
            "chemical": "Mancozeb or Myclobutanil",
            "chemical_image": "assets/Mancozeb.jpeg",
            "procedure": [
                "Apply fungicide at the first sign of infection.",
                "Remove and destroy infected leaves and fruit.",
                "Ensure good air circulation by proper pruning.",
                "Use resistant grape varieties if available."
            ],
            "expected_outcome": "Healthy grapevines with no black rot infection.",
            "healthy_image": "assets/grape_healthy.jpg"
        },
        "Grape___Esca_(Black_Measles)": {
            "disease_image": "https://example.com/grape_esca.jpeg",
            "chemical": "Triazole-based fungicides",
            "chemical_image": "assets/Trizole.jpg",
            "procedure": [
                "Prune and remove infected wood.",
                "Avoid injuring vines to reduce infection risk.",
                "Apply fungicide early in the growing season.",
                "Monitor vines regularly and ensure proper nutrition."
            ],
            "expected_outcome": "Vines free from Esca disease, ensuring better grape yield.",
            "healthy_image": "assets/grape_healthy.jpg"
        },
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
            "disease_image": "https://example.com/grape_leaf_blight.jpg",
            "chemical": "Copper-based fungicides",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply copper fungicide at early infection stage.",
                "Remove infected leaves to prevent spread.",
                "Maintain proper plant spacing for airflow.",
                "Implement crop rotation to prevent reinfection."
            ],
            "expected_outcome": "Healthy grape leaves with no signs of blight.",
            "healthy_image": "assets/grape_healthy.jpg"
        },
        "Grape___healthy": {
            "disease_image": "assets/grape_healthy.jpgg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical2.jpg",
            "procedure": [
                "Ensure regular pruning for better air circulation.",
                "Provide adequate watering and nutrient supply.",
                "Monitor vines regularly for pests and diseases.",
                "Use mulch to retain soil moisture and suppress weeds."
            ],
            "expected_outcome": "Healthy grapevines with high-quality fruit production.",
            "healthy_image": "assets/grape_healthy.jpg"
        },
        "Orange___Haunglongbing_(Citrus_greening)": {
            "disease_image": "assets/orangecitrus.jpeg",
            "chemical": "Oxytetracycline or Streptomycin",
            "chemical_image": "assets/Oxytetracycline1.jpeg",
            "procedure": [
                "Remove and destroy infected trees to prevent spread.",
                "Apply antibiotics as a foliar spray or trunk injection.",
                "Control psyllid populations using approved insecticides.",
                "Ensure balanced nutrition and proper irrigation."
            ],
            "expected_outcome": "Reduced spread of citrus greening and improved tree health.",
            "healthy_image": "assets/healthy_orange.jpeg"
        },
        "Peach___Bacterial_spot": {
            "disease_image": "assets/peachbactirialspot.jpeg",
            "chemical": "Copper-based bactericides",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply copper sprays during dormancy and early season.",
                "Remove and destroy infected leaves and twigs.",
                "Avoid overhead irrigation to reduce moisture.",
                "Use resistant peach varieties when planting."
            ],
            "expected_outcome": "Peach trees with reduced bacterial spot infections.",
            "healthy_image": "assets/peach__healthy.jpeg"
        },
        "Peach___healthy": {
            "disease_image": "assets/peach__healthy.jpeg",
            "chemical": "No treatment needed",
            "procedure": [
                "Provide regular watering and fertilization.",
                "Monitor trees for early signs of disease.",
                "Prune trees to improve air circulation.",
                "Use mulch to maintain soil moisture and suppress weeds."
            ],
            "expected_outcome": "Healthy peach trees with high fruit yield.",
            "healthy_image": "assets/peach__healthy.jpeg"
        },
        "Pepper,_bell___Bacterial_spot": {
            "disease_image": "assets/Pepper,_bell___Bacterial_spot.jpeg",
            "chemical": "Copper-based bactericides or Streptomycin",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply copper-based bactericide at early infection stages.",
                "Remove infected leaves and avoid overhead irrigation.",
                "Rotate crops to prevent soil contamination.",
                "Use resistant pepper varieties when available."
            ],
            "expected_outcome": "Bell pepper plants free from bacterial spot.",
            "healthy_image": "assets/Pepper,_bell___healthy.jpeg"
        },
        "Pepper,_bell___healthy": {
            "disease_image": "assets/Pepper,_bell___healthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical1.jpg",
            "procedure": [
                "Ensure proper fertilization and watering.",
                "Monitor plants for early signs of disease.",
                "Practice crop rotation to maintain soil health.",
                "Maintain proper spacing for airflow and disease prevention."
            ],
            "expected_outcome": "Healthy bell pepper plants with high yield.",
            "healthy_image": "Pepper,_bell___healthy"
        },
        "Raspberry___healthy": {
            "disease_image": "assets/Raspberry___healthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical3.jpg",
            "procedure": [
                "Ensure well-drained soil and proper watering.",
                "Prune canes to improve air circulation.",
                "Monitor for early signs of disease or pests.",
                "Use mulch to maintain soil moisture and prevent weeds."
            ],
            "expected_outcome": "Healthy raspberry plants with high fruit yield.",
            "healthy_image": "assets/Raspberry___healthy.jpeg"
        },
        "Soybean___healthy": {
            "disease_image": "assets/Soybean___healthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical3.jpg",
            "procedure": [
                "Rotate crops to prevent disease buildup in the soil.",
                "Ensure proper fertilization and irrigation.",
                "Monitor for pests and apply control measures as needed.",
                "Use disease-resistant soybean varieties when planting."
            ],
            "expected_outcome": "Healthy soybean plants with optimal growth.",
            "healthy_image": "assets/Soybean___healthy.jpeg"
        },
        "Squash___Powdery_mildew": {
            "disease_image": "Squash___Powdery_mildew.jpeg",
            "chemical": "Sulfur or Potassium bicarbonate",
            "chemical_image": "assets/sulfur.jpeg",
            "procedure": [
                "Apply sulfur-based fungicide at early signs of infection.",
                "Ensure good air circulation by proper plant spacing.",
                "Water plants at the base to avoid leaf moisture.",
                "Remove heavily infected leaves to prevent spread."
            ],
            "expected_outcome": "Squash plants with reduced mildew infection.",
            "healthy_image": "assets/healthy_squash.jpeg"
        },
        "Strawberry___Leaf_scorch": {
            "disease_image": "Strawberry___Leaf_scorch.jpeg",
            "chemical": "Copper-based fungicides",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply copper fungicides during early disease development.",
                "Prune affected leaves and remove plant debris.",
                "Ensure adequate watering and avoid overhead irrigation.",
                "Use resistant strawberry varieties if available."
            ],
            "expected_outcome": "Strawberry plants with minimal leaf scorch and healthy growth.",
            "healthy_image": "assets/Strawberry___healthy.jpeg"
        },
        "Strawberry___healthy": {
            "disease_image": "assets/Strawberry___healthy.jpeg",
            "chemical": "No treatment needed",
            "procedure": [
                "Ensure proper soil drainage and watering routine.",
                "Monitor plants for early signs of pests or disease.",
                "Use mulch to retain soil moisture and prevent weeds.",
                "Fertilize appropriately for better fruit production."
            ],
            "expected_outcome": "Healthy strawberry plants with high fruit yield.",
            "healthy_image": "assets/Strawberry___healthy.jpeg"
        },
        "Tomato___Bacterial_spot": {
            "disease_image": "assets/Tomato___Bacterial_spot.jpeg",
            "chemical": "Copper-based fungicide or Streptomycin",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply copper-based fungicide at early signs of infection.",
                "Avoid overhead watering to reduce bacterial spread.",
                "Remove infected leaves and debris from the plant base.",
                "Rotate crops to prevent recurring infections."
            ],
            "expected_outcome": "Tomato plants with reduced bacterial spot infection.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Early_blight": {
            "disease_image": "assets/Tomato___Early_blight.jpeg",
            "chemical": "Chlorothalonil or Copper fungicide",
            "chemical_image": "assets/chlorothalonil.jpeg",
            "procedure": [
                "Apply fungicide at the first sign of infection.",
                "Ensure proper spacing for good air circulation.",
                "Water plants at the base to avoid wetting leaves.",
                "Remove and destroy infected leaves."
            ],
            "expected_outcome": "Healthy tomato plants with no signs of early blight.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Late_blight": {
            "disease_image": "assets/Tomato___Late_blight.jpeg",
            "chemical": "Mancozeb or Metalaxyl",
            "chemical_image": "assets/Mancozeb.jpeg",
            "procedure": [
                "Apply fungicide at early symptoms.",
                "Ensure good airflow between plants.",
                "Remove and dispose of infected plant parts.",
                "Monitor humidity levels to reduce blight conditions."
            ],
            "expected_outcome": "Tomato plants with minimal blight infection.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Leaf_Mold": {
            "disease_image": "assets/Tomato___Leaf_Mold.jpeg",
            "chemical": "Chlorothalonil or Copper fungicide",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply fungicide at early signs of leaf mold.",
                "Ensure plants receive adequate sunlight and air circulation.",
                "Water at the base of the plant and avoid leaf moisture.",
                "Remove and destroy infected leaves."
            ],
            "expected_outcome": "Healthy tomato plants with no leaf mold.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Septoria_leaf_spot": {
            "disease_image": "assets/Tomato___Septoria_leaf_spot.jpeg",
            "chemical": "Copper-based fungicide",
            "chemical_image": "assets/copperfungicide.jpeg",
            "procedure": [
                "Apply fungicide at early signs of infection.",
                "Remove and destroy infected leaves.",
                "Ensure good air circulation by proper spacing.",
                "Mulch soil to prevent fungal spores from splashing onto leaves."
            ],
            "expected_outcome": "Tomato plants with reduced risk of Septoria leaf spot.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Spider_mites_Two-spotted_spider_mite": {
            "disease_image": "Tomato___Spider_mites_Two-spotted_spider_mite.jpeg",
            "chemical": "Neem_oil or Insecticidal soap",
            "chemical_image": "assets/neem_oil.jpeg",
            "procedure": [
                "Spray neem oil or insecticidal soap on infested plants.",
                "Increase humidity to deter spider mites.",
                "Introduce natural predators like ladybugs.",
                "Remove and destroy heavily infested leaves."
            ],
            "expected_outcome": "Tomato plants free from spider mites and healthy foliage.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Target_Spot": {
            "disease_image": "assets/Tomato___Target_Spot.jpeg",
            "chemical": "Mancozeb or Copper-based fungicide",
            "chemical_image": "assets/Mancozeb.jpeg",
            "procedure": [
                "Apply fungicide at early disease signs.",
                "Remove infected leaves and destroy them.",
                "Ensure good air circulation by spacing plants.",
                "Avoid overhead irrigation to reduce moisture buildup."
            ],
            "expected_outcome": "Tomato plants with no target spot infection.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
            "disease_image": "assets/Tomato___Tomato_Yellow_Leaf_Curl_Virus.jpeg",
            "chemical": "No chemical treatment, manage whiteflies",
            "chemical_image": "added/chemical1.jpg",
            "procedure": [
                "Use reflective mulch to repel whiteflies.",
                "Introduce natural predators like ladybugs.",
                "Remove and destroy infected plants.",
                "Plant virus-resistant tomato varieties."
            ],
            "expected_outcome": "Healthy tomato plants with no viral infection.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___Tomato_mosaic_virus": {
            "disease_image": "assets/Tomato___Tomato_mosaic_virus.jpeg",
            "chemical": "No chemical treatment, control aphids",
            "chemical_image": "added/chemical1.jpg",
            "procedure": [
                "Control aphids with insecticidal soap.",
                "Sanitize hands and tools before handling plants.",
                "Remove and destroy infected plants.",
                "Use virus-resistant tomato varieties."
            ],
            "expected_outcome": "Healthy tomato plants without mosaic virus symptoms.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        },
        "Tomato___healthy": {
            "disease_image": "assets/Tomato___healthy.jpeg",
            "chemical": "No treatment needed",
            "chemical_image": "added/chemical3.jpg",
            "procedure": [
                "Ensure proper soil nutrients and watering schedule.",
                "Monitor for pests and diseases regularly.",
                "Stake or cage plants to prevent contact with soil.",
                "Rotate crops to maintain soil health."
            ],
            "expected_outcome": "Healthy tomato plants with high yield.",
            "healthy_image": "assets/Tomato___healthy.jpeg"
        }
    }
    return recommendations.get(disease, None)


st.title("Crop Disease Treatment Recommendations")
disease = st.selectbox("Select the detected disease:", [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy", "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_", "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
    "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy", "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot",
    "Peach___healthy", "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot",
    "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
])

data = get_recommendation(disease)

if data:
    st.subheader("Disease Overview")
    st.image(data["disease_image"], caption=disease.replace("_", " "), use_container_width=True)

    st.subheader("Recommended Treatment")
    st.write(f"**Chemical:** {data['chemical']}")
    st.image(data["chemical_image"], caption=data['chemical'], use_container_width=True)

    st.subheader("Application Procedure")
    for step in data["procedure"]:
        st.write(f"- {step}")

    st.subheader("Expected Outcome")
    st.image(data["healthy_image"], caption=data["expected_outcome"], use_container_width=True)
else:
    st.warning("No recommendation found for the selected disease. More will be added soon!")
