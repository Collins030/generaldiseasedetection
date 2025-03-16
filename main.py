import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import communityfoumupdate  # Import your community page
import recommendation #import recommendation page

# Tensorflow Model Prediction
# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("model/trained_plant_disease_model2.keras")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    confidence = np.max(predictions) * 100  # Get confidence percentage
    return np.argmax(predictions), confidence  # return index and confidence percentage

# Sidebar
#st.sidebar.title("Dashboard")
#app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition", "Community","Disease Recommendation"])  # Added Community recommendation
#myadded code
st.sidebar.title("Dashboard")

# Pages dictionary with icons
pages = {
    "Home": "🏠",
    "About": "ℹ️",
    "Disease Recognition": "🔬",
    "Disease Recommendation": "🩺"
}

# Store selected page in session state
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Loop through pages to create buttons
for page, icon in pages.items():
    if st.sidebar.button(f"{icon} {page}"):
        st.session_state["page"] = page  # Update selected page

app_mode = st.session_state["page"]  # Use selected page for navigation

#end of addedd code
# Main Page
if app_mode == "Home":
    st.header("PLANT DISEASE RECOGNITION SYSTEM")
    image_path = "home_page.jpeg"
    st.image(image_path, use_container_width=True)
    st.markdown("""Welcome to the Plant Disease Recognition System! 🌿🔍
    Welcome to the Plant Disease Recognition System! 🌿🔍

    Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

    ### How It Works
    1. **Upload Image:** Go to the **Disease Recognition** page and upload an image of a plant with suspected diseases.
    2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
    3. **Results:** View the results and recommendations for further action.

    ### Why Choose Us?
    - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant Disease Recognition System!

    ### About Us
    Learn more about the project, our team, and our goals on the **About** page.
    """)

elif app_mode == "About":
    st.header("About")
    st.markdown("""
    #### About Dataset
    This dataset consists of 87K RGB images of healthy and diseased crop leaves categorized into 38 classes.
    """)

    # Accuracy Data
    categories = [
        "Apple", "Blueberry", "Cherry", "Corn", "Grape", "Orange", "Peach", "Pepper", "Potato", "Raspberry", "Soybean",
        "Squash", "Strawberry", "Tomato"
    ]
    accuracies = [0.97, 0.98, 0.99, 0.96, 0.99, 0.98, 0.98, 0.97, 0.97, 0.99, 0.97, 0.99, 0.99, 0.95]

    # Training History
    epochs = list(range(1, 11))
    history = {
        'accuracy': [0.592, 0.858, 0.911, 0.937, 0.953, 0.965, 0.969, 0.973, 0.978, 0.981],
        'loss': [1.385, 0.451, 0.273, 0.191, 0.140, 0.106, 0.090, 0.079, 0.064, 0.059],
        'val_accuracy': [0.819, 0.889, 0.939, 0.922, 0.926, 0.954, 0.947, 0.956, 0.945, 0.971],
        'val_loss': [0.574, 0.346, 0.189, 0.243, 0.229, 0.148, 0.174, 0.147, 0.210, 0.094]
    }

    # Create DataFrame
    df = pd.DataFrame({"Crop": categories, "Accuracy": [a * 100 for a in accuracies]})

    # Plot Accuracy for Different Crops
    st.subheader("Model Accuracy Across Different Crops")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Accuracy", y="Crop", data=df, palette="viridis")
    plt.xlabel("Accuracy (%)")
    plt.ylabel("Crops")
    plt.xlim(90, 100)
    plt.title("Model Accuracy for Different Crops")
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    st.pyplot(plt)

    # Plot Training History
    st.subheader("Training History")
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    ax1.plot(epochs, history['accuracy'], 'bo-', label='Training Accuracy')
    ax1.plot(epochs, history['val_accuracy'], 'go-', label='Validation Accuracy')
    ax2.plot(epochs, history['loss'], 'r--', label='Training Loss')
    ax2.plot(epochs, history['val_loss'], 'm--', label='Validation Loss')

    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Accuracy")
    ax2.set_ylabel("Loss")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.title("Training and Validation Accuracy & Loss")
    st.pyplot(fig)

elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image:")
    if st.button("Show Image"):
        st.image(test_image, use_column_width=True)

    if st.button("Predict"):
        st.snow()
        st.write("Our Prediction")
        result_index, confidence = model_prediction(test_image)

        class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                      'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
                      'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                      'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
                      'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                      'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                      'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                      'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                      'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                      'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
                      'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
                      'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
                      'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                      'Tomato___healthy']

        st.success(f"Model is Predicting it's a {class_name[result_index]}")

        # Display accuracy percentage
        st.write(f"Prediction Confidence: {confidence:.2f}%")

        # Display progress bar with accuracy rating
        rating = "Poor"
        if confidence > 90:
            rating = "Excellent"
        elif confidence > 80:
            rating = "Very Good"
        elif confidence > 70:
            rating = "Good"
        elif confidence > 60:
            rating = "Fair"

        st.progress(float(confidence) / 100)
        st.write(f"Accuracy Level: **{rating}**")

#elif app_mode == "Community":
    #communityfoumupdate.community_page()  # Call the community function
elif app_mode == "Disease Recommendation":
    st.title("Disease Treatment Recommendation")
    disease = st.selectbox("Select Detected Disease:", [
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

    data = recommendation.get_recommendation(disease)  # Call the function with user selection

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

