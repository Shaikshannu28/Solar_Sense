let voiceEnabled = true;

function toggleVoice() {
  voiceEnabled = !voiceEnabled;
  document.getElementById("toggle-voice").innerText = voiceEnabled ? "🔈" : "🔇";
}

function speak(text) {
  if (!voiceEnabled) return;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  speechSynthesis.speak(utterance);
}

let recognition;
let synth = window.speechSynthesis;

function initVoiceAssistant() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Your browser does not support Speech Recognition.");
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = async function (event) {
    const transcript = event.results[0][0].transcript;
    console.log("User:", transcript);
    speakText("Let me check...");
    sendQueryToBackend(transcript);
  };

  recognition.onerror = function (event) {
    console.error("Speech Recognition Error:", event.error);
  };
}

function startListening() {
  speakText("Hey, I'm Sol! How can I help you today?");
  if (recognition) {
    recognition.start();
  }
}

async function sendQueryToBackend(query) {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: query }),
    });

    const data = await res.json();
    const reply = data.reply;
    console.log("Bot:", reply);
    speakText(reply);
  } catch (error) {
    console.error("Error fetching chatbot reply:", error);
    speakText("Sorry, I couldn't connect to the assistant.");
  }
}

function speakText(text) {
  if (synth.speaking) synth.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-US';
  synth.speak(utter);
}

// Floating button setup
window.onload = function () {
  initVoiceAssistant();
  const btn = document.createElement("button");
  btn.textContent = "🎙️ Ask Sol";
  btn.id = "mic-button";
  btn.style.position = "fixed";
  btn.style.bottom = "20px";
  btn.style.right = "20px";
  btn.style.padding = "10px 20px";
  btn.style.background = "#28a745";
  btn.style.color = "#fff";
  btn.style.border = "none";
  btn.style.borderRadius = "50px";
  btn.style.cursor = "pointer";
  btn.style.zIndex = 1000;
  btn.onclick = startListening;
  document.body.appendChild(btn);
};
