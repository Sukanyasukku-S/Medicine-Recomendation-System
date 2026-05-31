import joblib
import pandas as pd
import numpy as np

from utils.preprocess import normalize_symptoms

model = joblib.load("model/disease_model.pkl")
symptom_encoder = joblib.load("model/symptom_encoder.pkl")
disease_encoder = joblib.load("model/disease_encoder.pkl")

details_df = pd.read_csv("dataset/disease_details.csv")

VALID_SYMPTOMS = list(symptom_encoder.classes_)

def predict_disease(user_input):
    symptoms = normalize_symptoms(user_input, VALID_SYMPTOMS)

    print("User Input:", user_input)
    print("Detected Symptoms:", symptoms)

    if len(symptoms) < 0:
        return {
            "status": "low_input",
            "message": "Please enter at least 2 or 3 symptoms for better prediction.",
            "symptoms": symptoms
        }

    X = symptom_encoder.transform([symptoms])
    probabilities = model.predict_proba(X)[0]

    best_index = int(np.argmax(probabilities))
    confidence = float(probabilities[best_index])

    disease = disease_encoder.inverse_transform([best_index])[0]

    disease_info = details_df[details_df["Disease"] == disease]

    if disease_info.empty:
        return {
            "status": "error",
            "message": "Disease details not found in dataset.",
            "disease": disease
        }

    row = disease_info.iloc[0].to_dict()

    return {
        "status": "success",
        "disease": disease,
        "confidence": round(confidence * 100, 2),
        "symptoms": symptoms,
        "description": row["Description"],
        "precaution": row["Precaution"],
        "medication": row["Medication"],
        "diet": row["Diet"],
        "workout": row["Workout"],
        "note": "This is an AI-based prediction for educational purposes only. Please consult a doctor for medical confirmation."
    }