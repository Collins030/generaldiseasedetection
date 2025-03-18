import streamlit as st
import requests
from io import BytesIO

def uploads_page():
    st.title("Uploads Page")
    st.write("Download sample images and upload them for disease detection.")
    st.write("After downloading, return to the Disease Recognition tab to upload your image.")

    # Dictionary of sample images (Replace with actual URLs from your GitHub)
    sample_images = {
        "Apple Cedar Rust": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleCedarRust1.JPG",
        "Apple Scab 1": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/AppleScab1.JPG",
        "Potato Early Blight 3": "https://raw.githubusercontent.com/Collins030/generaldiseasedetection/main/test/test/PotatoEarlyBlight3.JPG",
    }

    # Create columns dynamically
    num_cols = len(sample_images)
    cols = st.columns(num_cols)  # Create one column per image

    for col, (name, url) in zip(cols, sample_images.items()):
        response = requests.get(url)

        if response.status_code == 200:
            image_bytes = BytesIO(response.content)

            with col:
                st.image(image_bytes, caption=name, width=128)  # Show image
                st.download_button(
                    label=f"Download {name}",
                    data=image_bytes.getvalue(),
                    file_name=f"{name.replace(' ', '_')}.jpg",
                    mime="image/jpeg"
                )
        else:
            st.error(f"Failed to load {name}. Check the image URL.")


if __name__ == "__main__":
    uploads_page()
