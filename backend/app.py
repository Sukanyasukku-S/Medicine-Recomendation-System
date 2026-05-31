from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.predictor import predict_disease, VALID_SYMPTOMS
from utils.chatbot import chatbot_reply

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Medicine Recommendation System Backend is running successfully",
        "total_symptoms": len(VALID_SYMPTOMS),
        "available_symptoms": VALID_SYMPTOMS
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "symptoms" not in data:
        return jsonify({
            "status": "error",
            "message": "Please provide symptoms."
        }), 400

    user_symptoms = data["symptoms"]

    result = predict_disease(user_symptoms)
    result["chatbot"] = chatbot_reply(result)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)