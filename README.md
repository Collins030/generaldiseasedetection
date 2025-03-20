# 🌿 General Plant Disease Detection System 🌱

Welcome to the **General Plant Disease Detection System**! This project leverages machine learning and web development to help users identify and receive treatment recommendations for various plant diseases. 🌾🦠

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation Guide](#installation-guide)
4. [Usage Instructions](#usage-instructions)
5. [Technologies Used](#technologies-used)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact Information](#contact-information)

## Project Overview

The General Plant Disease Detection System is designed to:

- **Identify Plant Diseases:** Upload an image of a plant leaf, and the system predicts the disease affecting it.
- **Provide Treatment Recommendations:** Based on the identified disease, receive detailed treatment options, including chemicals, application procedures, and expected outcomes.

## Features

- **Disease Recognition:** 📸
  - Upload plant leaf images for disease identification.
  - Receive predictions with confidence levels.
- **Treatment Recommendations:** 💊
  - Access disease-specific treatment options.
  - View application procedures and expected outcomes.
- **User-Friendly Interface:** 🖥️
  - Streamlit-based web application for easy navigation.
  - Interactive elements like image uploaders and selectors.

## Installation Guide

To set up the General Plant Disease Detection System locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Collins030/generaldiseasedetection.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd generaldiseasedetection
   ```

3. **Set Up a Virtual Environment (Optional but Recommended):**

   - For **Windows**:

     ```bash
     python -m venv env
     env\Scripts\activate
     ```

   - For **macOS/Linux**:

     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

4. **Install Dependencies:**

   Ensure you have `pip` installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**

   Start the Streamlit app with:

   ```bash
   streamlit run app.py
   ```

   Open your browser and navigate to `http://localhost:8501` to access the application.

## Usage Instructions

1. **Disease Recognition:**
   - On the homepage, click on the "Disease Recognition" option from the sidebar.
   - Upload a clear image of the plant leaf you wish to analyze.
   - The system will process the image and display the predicted disease along with the confidence level.

2. **Treatment Recommendations:**
   - After obtaining a disease prediction, navigate to the "Disease Recommendation" page.
   - Select the detected disease from the dropdown menu.
   - View the recommended treatment, including chemical treatments, application procedures, and expected outcomes.

## Technologies Used

- **Streamlit:** 🖥️
  - Framework for building the web application interface.
- **TensorFlow/Keras:** 🤖
  - Machine learning libraries used for model development.
- **OpenCV:** 🖼️
  - Image processing library for handling image uploads.
- **Pandas & NumPy:** 🔢
  - Data manipulation and numerical operations.
- **scikit-learn:** 📊
  - Machine learning library for model evaluation.

## Contributing

We welcome contributions to enhance the functionality and accuracy of the General Plant Disease Detection System. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your forked repository (`git push origin feature-name`).
5. Submit a pull request detailing your changes.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information

For inquiries or feedback, please contact:

- **Email:** ##
- **GitHub:** [https://github.com/Collins030](https://github.com/Collins030)

We hope this system aids in the effective identification and treatment of plant diseases, contributing to healthier crops and gardens! 🌿🌱 
