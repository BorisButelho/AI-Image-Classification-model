# AI Image Classification Model (CNN) 

An AI-powered mobile + backend system designed to identify Hindu deities and sacred iconographic symbols from temple statues, paintings, idols, and religious artwork using image-based deep learning.

The user captures an image through the mobile app camera, and the system analyzes the image to predict the deity, detect symbolic attributes, and generate a detailed explanation.

---

# Project Overview

Indian temple iconography contains rich symbolic representations such as:

- Trident (Shiva)
- Conch (Vishnu)
- Lotus (Lakshmi)
- Flute (Krishna)
- Mouse (Ganesha)
- Lion (Durga)
- Swan / Veena (Saraswati)

This project uses computer vision and deep learning to recognize such features and infer the most likely deity automatically.

---

# Key Features

- Android mobile camera capture using Expo React Native
- Real-time image upload to Python Flask backend
- Deep learning based deity detection
- Symbol / object recognition from image
- Narrative explanation engine
- Confidence-based reasoning
- Clean dark themed mobile UI
- Resume-ready full stack AI project

---

# Tech Stack

## Frontend (Mobile App)

- React Native
- Expo
- TypeScript
- Expo Camera

## Backend

- Python
- Flask
- Flask-CORS

## AI / ML

- YOLOv8 Object Detection
- CNN-based image learning pipeline
- Custom labeled dataset
- Confidence score filtering
- Rule-based correlation engine

---

# How It Works

## Step 1 – User Captures Image

The user opens the Android mobile app and captures a photo of a deity idol, painting, or sculpture.

## Step 2 – Image Sent to Backend

The image is sent from React Native frontend to Flask API.

## Step 3 – AI Detection

The trained model detects:

- deity faces/forms
- weapons
- animals
- sacred symbols
- iconographic markers

## Step 4 – Correlation Engine

Detected labels are matched with deity-symbol rules.

Example:

- Shiva + Trident + Serpent = Shiva
- Ganesha + Mouse = Ganesha
- Vishnu + Conch + Chakra = Vishnu

## Step 5 – Explanation Generated

The system returns:

- Main deity name
- Confidence score
- Symbols found
- Cultural significance
- Narrative explanation

---

# Model Training

The model was trained on a custom dataset containing multiple deity classes and symbolic classes.

## Example Classes

- Shiva
- Vishnu
- Ganesha
- Durga
- Lakshmi
- Krishna
- Hanuman
- Rama
- Saraswati

## Symbol Classes

- Trident
- Conch
- Chakra
- Lotus
- Flute
- Serpent
- Lion
- Mouse
- Bull

---

# Accuracy Improvement Techniques

- Dataset balancing
- Image labeling refinement
- Confidence threshold tuning
- Duplicate label filtering
- Correlation score boosting
- Dominance filtering for single deity images
- Generalization using multiple image styles

---

# Challenges Solved

## Multi-Deity Misclassification

Resolved using dominance score logic.

## Duplicate Predictions

Removed repeated labels while keeping highest confidence.

## Generalization

Used statues, paintings, idols, posters, temple carvings.

## Mobile Integration

Connected AI backend with Android camera app.

