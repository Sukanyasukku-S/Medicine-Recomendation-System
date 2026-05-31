async function predictDisease() {
    const symptoms = document.getElementById("symptomsInput").value.trim();
    const resultSection = document.getElementById("resultSection");

    if (symptoms === "") {
        alert("Please enter symptoms first.");
        return;
    }

    resultSection.classList.remove("hidden");
    document.getElementById("disease").innerText = "Loading...";
    document.getElementById("description").innerText = "Please wait, predicting disease...";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ symptoms: symptoms })
        });

        const data = await response.json();
        console.log("Backend Response:", data);

        if (data.status !== "success") {
            document.getElementById("disease").innerText = "Need More Symptoms";
            document.getElementById("confidence").innerText = "";
            document.getElementById("description").innerText = data.message;
            document.getElementById("precaution").innerText = "-";
            document.getElementById("medication").innerText = "-";
            document.getElementById("diet").innerText = "-";
            document.getElementById("workout").innerText = "-";
            document.getElementById("chatbot").innerText = data.chatbot || data.message;
            document.getElementById("note").innerText = "Enter symptoms like: fever, cough, headache, body pain";
            return;
        }

        document.getElementById("disease").innerText = data.disease;
        document.getElementById("confidence").innerText = "Confidence: " + data.confidence + "%";
        document.getElementById("description").innerText = data.description;
        document.getElementById("precaution").innerText = data.precaution;
        document.getElementById("medication").innerText = data.medication;
        document.getElementById("diet").innerText = data.diet;
        document.getElementById("workout").innerText = data.workout;
        document.getElementById("chatbot").innerText = data.chatbot;
        document.getElementById("note").innerText = data.note;

        resultSection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        console.log("Error:", error);
        document.getElementById("disease").innerText = "Connection Error";
        document.getElementById("description").innerText = "Backend is not running. Start backend using python app.py";
    }
}
