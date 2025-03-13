
# AI Pneumonia Detector

## Overview

This project is an AI-powered pneumonia detection system that uses deep learning and Google Gemini for image analysis. The goal of this project is to classify X-ray images into two categories: **Normal** and **Pneumonia**. The model is built using a pre-trained **VGG19** network fine-tuned for pneumonia detection. The system can be run using **Streamlit**, providing an interactive user interface.

## Features

- **Pneumonia Detection**: Classify X-ray images into Normal or Pneumonia.
- **AI Analysis with Gemini**: Provides medical analysis of X-ray images using Google Gemini.
- **Interactive UI**: Upload X-ray images and get predictions and detailed explanations through an easy-to-use web interface.

## Requirements

- Python 3.x
- `tensorflow` for model loading and prediction.
- `streamlit` for the user interface.
- `opencv-python` for image processing.
- `requests` for sending requests to the Google Gemini API.
- `PIL` for image loading and manipulation.

## Installation

To run this project, you need to install the required libraries. You can use the following command to install the dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, you can install them individually:

```bash
pip install tensorflow streamlit opencv-python requests pillow
```

### Set up the Gemini API Key

This project uses Google Gemini API for generating medical analysis for the uploaded X-ray images. To use the AI analysis feature, you need to set your **Gemini API Key**.

1. Obtain the Gemini API Key from [Google Gemini](https://cloud.google.com/ai).
2. Set the API key in your environment variables:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Alternatively, you can replace the environment variable directly in the code.

## Running the Application

After setting up the environment and dependencies, you can start the Streamlit application by running:

```bash
streamlit run app.py
```

This will open the application in your web browser.

## How It Works

1. **Upload X-ray Image**: The user uploads an X-ray image in the sidebar of the Streamlit application.
2. **Model Prediction**: The image is processed by a pre-trained **VGG19** model to predict if the X-ray shows normal or pneumonia features.
3. **AI Analysis**: Google Gemini API is called to provide an additional AI-driven explanation of the image.
4. **Results Display**: The prediction result (Normal or Pneumonia) is displayed with a confidence score. Additionally, the detailed analysis of the image is shown using Google Gemini.

## Example of Output

- **Prediction**: Pneumonia
- **Confidence**: 95.4%

> **AI Explanation**: The X-ray shows clear signs of pneumonia, with unusual cloud-like patterns indicating infection in the lungs. The infection may require immediate medical attention.

## Disclaimer

The results of this application are not a substitute for medical diagnosis. Please consult a healthcare professional for a proper diagnosis.

## Developer

- **Farrel0xx**

Feel free to follow me on [GitHub](https://github.com/Farrel0xx) and [YouTube](https://youtube.com/@Farrel0xx).

## License

This project is licensed under the MIT License.
