import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import upcommunity
#import communityfoumupdate  # Import your community page #I have commented it so as to avoid technicalities deploying it in streamlit
import recommendation #import recommendation page
import upload
from PIL import Image, ImageDraw
import base64
from io import BytesIO

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
#st.sidebar.title("Dashboard")
# Load the image
logo_path = "assets/logo/logo.jpeg"  # Update if needed
logo = Image.open(logo_path)


# Make the image circular
def make_circular(img):
    size = (min(img.size), min(img.size))  # Make it a square
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    img = img.resize(size)
    circular_img = Image.new("RGBA", size, (255, 255, 255, 0))
    circular_img.paste(img, (0, 0), mask)

    return circular_img


circular_logo = make_circular(logo)


# Convert image to base64
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


logo_base64 = image_to_base64(circular_logo)

# Custom HTML & CSS for sidebar layout
sidebar_html = f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
        <h3 style="margin: 0; font-size: 20px;">General Disease Detection</h3>
    </div>
"""

# Display in Streamlit sidebar
st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)

# Pages dictionary with icons
pages = {
    "Home": "🏠",
    "About": "ℹ️",
    "Disease Recognition": "🔬",
    "Community": "💬",
    "Disease Recommendation": "🩺",
    "Uploads":"📲"
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
    # Page Header
    st.header("🌱 PLANT DISEASE RECOGNITION SYSTEM 🌿")
    
    # Background Image
    image_path = "background1.jpg"
    st.image(image_path, use_container_width=True)
    
    # Welcome Message
    st.markdown(
        """
        ## 👋 Welcome to the Plant Disease Recognition System! 
        
        This tool helps you identify plant diseases quickly and efficiently using Machine learning-powered image recognition. 🚀
        
        ### 🌟 How to Get Started:
        1️⃣ **Navigate to the Disease Recognition page** from the sidebar.  
        2️⃣ **Upload an image** of the plant leaf you want to analyze.  
        3️⃣ **The system will process** the image and provide a diagnosis.  
        4️⃣ **Download sample images** from the **Uploads** section and re-upload them for testing. 
        
        🔄 *Future updates will include real-time testing of samples!* 
        
        ### 🌾 Diseases Covered (38 Classes):
        **🍏 Apple:** Apple scab, Black rot, Cedar apple rust, Healthy  
        **🫐 Blueberry:** Healthy  
        **🍒 Cherry (including sour):** Powdery mildew, Healthy  
        **🌽 Corn (maize):** Cercospora leaf spot / Gray leaf spot, Common rust, Northern Leaf Blight, Healthy  
        **🍇 Grape:** Black rot, Esca (Black Measles), Leaf blight (Isariopsis Leaf Spot), Healthy  
        **🍊 Orange:** Haunglongbing (Citrus greening)  
        **🍑 Peach:** Bacterial spot, Healthy  
        **🌶️ Pepper (bell):** Bacterial spot, Healthy  
        **🥔 Potato:** Early blight, Late blight, Healthy  
        **🍓 Strawberry:** Leaf scorch, Healthy  
        **🍅 Tomato:** Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites (Two-spotted), Target Spot, Tomato Yellow Leaf Curl Virus, Tomato mosaic virus, Healthy  
        
        ⚡ *Start diagnosing your plants now!* 
        """
    )


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
    st.header("🌿 Disease Recognition 🔍")
    
    test_image = st.file_uploader("📂 Choose an Image:")
    
    if st.button("🖼️ Show Image"):
        st.image(test_image, use_column_width=True)
    
    if st.button("🤖 Predict"):
        st.snow()
        st.write("### 🏆 Our Prediction:")
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
    
        st.success(f"🌱 Model Prediction: **{class_name[result_index]}**")
    
        # Display accuracy percentage
        st.write(f"🎯 **Prediction Confidence:** {confidence:.2f}%")
    
        # Display progress bar with accuracy rating
        rating = "Poor"
        if confidence > 90:
            rating = "🌟 Excellent"
        elif confidence > 80:
            rating = "✅ Very Good"
        elif confidence > 70:
            rating = "👍 Good"
        elif confidence > 60:
            rating = "🟡 Fair"
    
        st.progress(float(confidence) / 100)
        st.write(f"📊 **Accuracy Level:** {rating}")
    
    # Message for Uploads Navigation
    st.markdown(
        """
        ## 📥 Download & Test Images Easily!  
    
        🔹 You can navigate to the **Uploads** section 📂 to **download sample images**.  
        🔹 After downloading, return to the **Disease Recognition** page 📸 to **upload the image** and test the model.  
    
        🚀 *Try it now and see how well the model performs!*  
        """, 
        unsafe_allow_html=True
    )


#elif app_mode == "Community":
    #communityfoumupdate.community_page()  # Call the community function
elif app_mode == "Community":
    upcommunity.community_page()  # Call the community function
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

elif app_mode == "Uploads":
    upload.uploads_page()  # Call the upload function

