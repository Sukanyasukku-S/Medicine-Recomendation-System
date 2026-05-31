import re

SYMPTOM_SYNONYMS = {
    "cold": ["runny_nose", "sneezing", "cough", "sore_throat"],
    "common cold": ["runny_nose", "sneezing", "cough", "sore_throat"],
    "running nose": ["runny_nose"],
    "runny nose": ["runny_nose"],
    "blocked nose": ["blocked_nose"],
    "nose block": ["blocked_nose"],
    "sneezing": ["sneezing"],
    "cough": ["cough"],
    "throat pain": ["sore_throat"],
    "sore throat": ["sore_throat"],

    "fever": ["fever"],
    "high fever": ["high_fever"],
    "mild fever": ["mild_fever"],
    "temperature": ["fever"],
    "viral": ["fever", "body_pain", "fatigue", "headache"],
    "body pain": ["body_pain"],
    "body ache": ["body_pain"],
    "weakness": ["weakness"],
    "tired": ["fatigue"],
    "tiredness": ["fatigue"],

    "headache": ["headache"],
    "head pain": ["headache"],
    "severe headache": ["severe_headache"],
    "migraine": ["headache", "nausea", "sensitivity_to_light"],

    "vomit": ["vomiting"],
    "vomiting": ["vomiting"],
    "nausea": ["nausea"],
    "loose motion": ["diarrhea"],
    "loose motions": ["diarrhea"],
    "diarrhea": ["diarrhea"],
    "stomach ache": ["stomach_pain"],
    "stomach pain": ["stomach_pain"],
    "acidity": ["acidity"],
    "gas": ["acidity", "bloating"],

    "rash": ["skin_rash"],
    "skin rash": ["skin_rash"],
    "itching": ["itching"],
    "skin problem": ["skin_rash", "itching"],
    "pimples": ["pimples"],
    "acne": ["pimples", "oily_skin"],

    "breathing problem": ["breathing_problem"],
    "breath problem": ["breathing_problem"],
    "shortness of breath": ["shortness_of_breath"],
    "wheezing": ["wheezing"],
    "chest pain": ["chest_pain"],
    "chest tightness": ["chest_tightness"],

    "eye pain": ["eye_pain"],
    "red eyes": ["red_eyes"],
    "itchy eyes": ["itchy_eyes"],
    "watery eyes": ["watery_eyes"],

    "burning urination": ["burning_urination"],
    "urine burning": ["burning_urination"],
    "frequent urination": ["frequent_urination"],
    "back pain": ["back_pain"],

    "ear pain": ["ear_pain"],
    "hearing loss": ["hearing_loss"],

    "sugar": ["frequent_urination", "increased_thirst", "fatigue"],
    "diabetes": ["frequent_urination", "increased_thirst", "fatigue"],
    "bp": ["headache", "dizziness"],
    "blood pressure": ["headache", "dizziness"]
}

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-Z0-9,\s_]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def normalize_symptoms(user_text, valid_symptoms):
    text = clean_text(user_text)
    found = set()

    # synonym matching
    for key, values in SYMPTOM_SYNONYMS.items():
        if key in text:
            for value in values:
                if value in valid_symptoms:
                    found.add(value)

    # comma separated matching
    parts = [p.strip().replace(" ", "_") for p in text.split(",")]

    for part in parts:
        if part in valid_symptoms:
            found.add(part)

    # direct dataset symptom matching
    for symptom in valid_symptoms:
        symptom_space = symptom.replace("_", " ")
        if symptom in text or symptom_space in text:
            found.add(symptom)

    return sorted(found)