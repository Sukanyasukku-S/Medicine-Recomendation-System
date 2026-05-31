def chatbot_reply(result):
    if result["status"] != "success":
        return result["message"]

    symptoms = ", ".join(result["symptoms"])

    return (
        f"Hello, I am MediBot. You entered these symptoms: {symptoms}. "
        f"Based on the symptom pattern, the system predicts {result['disease']}. "
        f"You can read the disease description, precautions, medication guidance, diet plan, and workout suggestions above. "
        f"Please remember this is only an AI-based health recommendation system, not a confirmed medical diagnosis. "
        f"If symptoms are severe, continue for many days, or become worse, please consult a doctor."
    )