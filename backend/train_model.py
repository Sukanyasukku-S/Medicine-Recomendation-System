import os
import joblib
import pandas as pd

from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = "dataset/disease_symptoms.csv"
MODEL_DIR = "model"

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH).fillna("")

symptom_cols = [col for col in df.columns if col.startswith("Symptom_")]

df["symptoms"] = df[symptom_cols].values.tolist()

df["symptoms"] = df["symptoms"].apply(
    lambda symptoms: [
        str(symptom).strip().lower()
        for symptom in symptoms
        if str(symptom).strip() != ""
    ]
)

augmented_data = []

for _, row in df.iterrows():
    disease = row["Disease"]
    symptoms = row["symptoms"]

    augmented_data.append([disease, symptoms])

    if len(symptoms) > 3:
        for i in range(len(symptoms)):
            new_symptoms = symptoms[:i] + symptoms[i + 1:]
            augmented_data.append([disease, new_symptoms])

train_df = pd.DataFrame(augmented_data, columns=["Disease", "symptoms"])

symptom_encoder = MultiLabelBinarizer()
X = symptom_encoder.fit_transform(train_df["symptoms"])

disease_encoder = LabelEncoder()
y = disease_encoder.fit_transform(train_df["Disease"])

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)

predictions = model.predict(X)

print("Training Accuracy:", accuracy_score(y, predictions))
print()
print(classification_report(y, predictions, target_names=disease_encoder.classes_))

joblib.dump(model, os.path.join(MODEL_DIR, "disease_model.pkl"))
joblib.dump(symptom_encoder, os.path.join(MODEL_DIR, "symptom_encoder.pkl"))
joblib.dump(disease_encoder, os.path.join(MODEL_DIR, "disease_encoder.pkl"))

print("Model training completed successfully.")
print("Model files saved inside model folder.")