import streamlit as st
from PIL import Image


def get_recommendation(disease):
    recommendations = {
        "Apple___Apple_scab": {
            "disease_image": "https://example.com/apple_scab.jpg",
            "chemical": "Captan or Myclobutanil",
            "chemical_image": "https://example.com/captan.jpg",
            "procedure": [
                "Apply Captan at the beginning of the growing season.",
                "Ensure thorough coverage on leaves and fruit.",
                "Reapply after heavy rainfall.",
                "Use resistant apple varieties when possible."
            ],
            "expected_outcome": "Apple trees with no scab infection and healthy fruit.",
            "healthy_image": "https://example.com/healthy_apple.jpg"
        },
        "Apple___Black_rot": {
            "disease_image": "https://example.com/apple_black_rot.jpg",
            "chemical": "Thiophanate-methyl or Captan",
            "chemical_image": "https://example.com/thiophanate.jpg",
            "procedure": [
                "Prune infected branches and remove affected fruit.",
                "Apply fungicide during the growing season.",
                "Keep orchard clean and well-ventilated.",
                "Monitor trees regularly for signs of infection."
            ],
            "expected_outcome": "Healthy apple trees free from black rot.",
            "healthy_image": "https://example.com/healthy_apple.jpg"
        },
        "Apple___Cedar_apple_rust": {
            "disease_image": "https://example.com/cedar_apple_rust.jpg",
            "chemical": "Myclobutanil or Mancozeb",
            "chemical_image": "https://example.com/myclobutanil.jpg",
            "procedure": [
                "Apply fungicide early in the season.",
                "Remove nearby cedar trees if possible.",
                "Prune affected branches.",
                "Repeat treatment as per label instructions."
            ],
            "expected_outcome": "Apple trees with no rust infection.",
            "healthy_image": "https://example.com/healthy_apple.jpg"
        },
        "Apple___healthy": {
            "disease_image": "https://example.com/healthy_apple.jpg",
            "chemical": "No treatment needed",
            "chemical_image": "https://example.com/no_treatment.jpg",
            "procedure": [
                "Maintain proper watering and fertilization.",
                "Regularly inspect plants for signs of disease.",
                "Keep orchard clean and remove debris.",
                "Use disease-resistant varieties when planting."
            ],
            "expected_outcome": "Healthy apple trees with high yield.",
            "healthy_image": "https://example.com/healthy_apple.jpg"
        },
        "Potato___Late_blight": {
            "disease_image": "https://example.com/potato_late_blight.jpg",
            "chemical": "Mancozeb or Metalaxyl",
            "chemical_image": "https://example.com/mancozeb.jpg",
            "procedure": [
                "Mix the recommended dose of Mancozeb with water.",
                "Spray evenly on the affected leaves, ensuring full coverage.",
                "Repeat treatment every 7-10 days, especially in wet conditions.",
                "Monitor plant condition and remove heavily infected leaves."
            ],
            "expected_outcome": "Healthy potato crop with no signs of blight.",
            "healthy_image": "https://example.com/healthy_potato.jpg"
        },
        # Add remaining 33 classes following the same format
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
    st.image(data["disease_image"], caption=disease.replace("_", " "), use_column_width=True)

    st.subheader("Recommended Treatment")
    st.write(f"**Chemical:** {data['chemical']}")
    st.image(data["chemical_image"], caption=data['chemical'], use_column_width=True)

    st.subheader("Application Procedure")
    for step in data["procedure"]:
        st.write(f"- {step}")

    st.subheader("Expected Outcome")
    st.image(data["healthy_image"], caption=data["expected_outcome"], use_column_width=True)
else:
    st.warning("No recommendation found for the selected disease. More will be added soon!")
