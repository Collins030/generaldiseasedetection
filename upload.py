import streamlit as st
import requests
from io import BytesIO

def uploads_page():
    st.title("Uploads Page")
    st.write("Download sample images and upload them for disease detection.")
    st.write("After downloading, return to the Disease Recognition tab to upload your image.")

    # Dictionary of sample images (Replace with actual URLs from your GitHub)
    sample_images = {
         "Apple Cedar Rust 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleCedarRust2.JPG",
    "Apple Cedar Rust 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleCedarRust3.JPG",
    "Apple Cedar Rust 4": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleCedarRust4.JPG",
    "Apple Scab 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleScab1.JPG",
    "Apple Scab 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleScab2.JPG",
    "Apple Scab 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleScab3.JPG",
    "Corn Common Rust 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/CornCommonRust1.JPG",
    "Corn Common Rust 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/CornCommonRust2.JPG",
    "Corn Common Rust 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/CornCommonRust3.JPG",
    "Potato Early Blight 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoEarlyBlight1.JPG",
    "Potato Early Blight 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoEarlyBlight2.JPG",
    "Potato Early Blight 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoEarlyBlight3.JPG",
    "Potato Early Blight 4": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoEarlyBlight4.JPG",
    "Potato Early Blight 5": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoEarlyBlight5.JPG",
    "Potato Healthy 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoHealthy1.JPG",
    "Potato Healthy 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoHealthy2.JPG",
    "Tomato Early Blight 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoEarlyBlight1.JPG",
    "Tomato Early Blight 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoEarlyBlight2.JPG",
    "Tomato Early Blight 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoEarlyBlight3.JPG",
    "Tomato Early Blight 4": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoEarlyBlight4.JPG",
    "Tomato Early Blight 5": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoEarlyBlight5.JPG",
    "Tomato Early Blight 6": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoEarlyBlight6.JPG",
    "Tomato Healthy 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoHealthy1.JPG",
    "Tomato Healthy 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoHealthy2.JPG",
    "Tomato Healthy 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoHealthy3.JPG",
    "Tomato Healthy 4": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoHealthy4.JPG",
    "Tomato Yellow Curl Virus 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoYellowCurlVirus1.JPG",
    "Tomato Yellow Curl Virus 2": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoYellowCurlVirus2.JPG",
    "Tomato Yellow Curl Virus 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoYellowCurlVirus3.JPG",
    "Tomato Yellow Curl Virus 4": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoYellowCurlVirus4.JPG",
    "Tomato Yellow Curl Virus 5": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoYellowCurlVirus5.JPG",
    "Tomato Yellow Curl Virus 6": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/TomatoYellowCurlVirus6.JPG"
    }

    max_cols = 3  # Set max images per row
    image_items = list(sample_images.items())

    # Loop to create rows
    for i in range(0, len(image_items), max_cols):
        cols = st.columns(max_cols)
        for col, (name, url) in zip(cols, image_items[i:i + max_cols]):
            response = requests.get(url)

            if response.status_code == 200:
                image_bytes = BytesIO(response.content)

                with col:
                    st.image(image_bytes, caption=name, width=128)
                    st.download_button(
                        label="Download",
                        data=image_bytes.getvalue(),
                        file_name=f"{name.replace(' ', '_')}.jpg",
                        mime="image/jpeg"
                    )
            else:
                with col:
                    st.error(f"Failed to load {name}")


if __name__ == "__main__":
    uploads_page()
