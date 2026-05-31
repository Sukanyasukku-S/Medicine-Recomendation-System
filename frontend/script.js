let voiceEnabled = true;
let currentSpeech = null;

function speakText(text) {

    if (!voiceEnabled) {
        return;
    }

    speechSynthesis.cancel();

    currentSpeech = new SpeechSynthesisUtterance(text);

    currentSpeech.lang = "en-US";
    currentSpeech.rate = 0.9;
    currentSpeech.pitch = 1;

    speechSynthesis.speak(currentSpeech);
}

function toggleVoice() {

    voiceEnabled = !voiceEnabled;

    const btn = document.getElementById("voiceControl");

    if (voiceEnabled) {

        btn.innerHTML = "🔊";

    } else {

        btn.innerHTML = "🔇";

        speechSynthesis.cancel();
    }
}

function toggleChatbot() {
    const chatWindow = document.getElementById("chatWindow");
    chatWindow.classList.toggle("hidden");
}

function addBotMessage(message) {
    const chatBody = document.getElementById("chatBody");
    chatBody.innerHTML += `<div class="bot-message">${message}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}

function addUserMessage(message) {
    const chatBody = document.getElementById("chatBody");
    chatBody.innerHTML += `<div class="user-message">${message}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}


function formatBullets(text) {
    if (!text) return "<ul><li>-</li></ul>";

    let items = text
        .split("•")
        .map(item => item.trim())
        .filter(item => item.length > 0);

    if (items.length === 0) {
        return "<ul><li>" + text + "</li></ul>";
    }

    return "<ul>" + items.map(item => `<li>${item}</li>`).join("") + "</ul>";
}

async function predictDisease() {
    const symptoms = document.getElementById("symptomsInput").value.trim();
    addUserMessage("My symptoms are: " + symptoms);
    addBotMessage("Thank you. I am checking your symptoms...");
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

        if (data.status !== "success") {
            document.getElementById("disease").innerText = "Need More Symptoms";
            document.getElementById("confidence").innerText = "";
            document.getElementById("description").innerText = data.message;
            document.getElementById("precaution").innerText = "-";
            document.getElementById("medication").innerText = "-";
            document.getElementById("diet").innerText = "-";
            document.getElementById("workout").innerText = "-";
            document.getElementById("chatbot").innerText = data.chatbot || data.message;
            addBotMessage(data.chatbot || data.message);
            speakText(data.chatbot || data.message);
            return;
        }

        document.getElementById("disease").innerText = data.disease;

        // remove confidence display
        document.getElementById("confidence").innerText = "";

        document.getElementById("description").innerHTML = formatBullets(data.description);
        document.getElementById("precaution").innerHTML = formatBullets(data.precaution);
        document.getElementById("medication").innerHTML = formatBullets(data.medication);
        document.getElementById("diet").innerHTML = formatBullets(data.diet);
        document.getElementById("workout").innerHTML = formatBullets(data.workout);

        document.getElementById("chatbot").innerText = data.chatbot;
        
        addBotMessage(`
    <b>Prediction completed ✅</b><br>
    <b>Disease:</b> ${data.disease}<br><br>
    <b>Description:</b>
    ${formatBullets(data.description)}
    <b>Precautions:</b>
    ${formatBullets(data.precaution)}
    <b>Diet:</b>
    ${formatBullets(data.diet)}
    <b>Workout:</b>
    ${formatBullets(data.workout)}
    <br><b>Note:</b> ${data.note}
`); 

const voiceText = `
You entered symptoms: ${symptoms}.
The predicted disease is ${data.disease}.
Description: ${data.description.replaceAll("•", "")}.
Precautions: ${data.precaution.replaceAll("•", "")}.
Diet: ${data.diet.replaceAll("•", "")}.
Workout: ${data.workout.replaceAll("•", "")}.
Please consult a doctor for medical confirmation.
`;

speakText(voiceText);

        resultSection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        document.getElementById("disease").innerText = "Connection Error";
        document.getElementById("description").innerText = "Backend is not running. Start backend using python app.py";
    }
}