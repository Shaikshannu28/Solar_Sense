from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import smtplib
from email.message import EmailMessage
from ai.predictor import generate_suggestion

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})


# --- Simulated Solar Data Generator ---
def generate_data():
    return {
        "generation": round(random.uniform(1.5, 4.5), 2),
        "usage": round(random.uniform(1.0, 5.0), 2),
        "battery": round(random.uniform(50, 100), 1),
        "co2_saved": round(random.uniform(5, 15), 2),
        "trees_saved": random.randint(10, 50),
        "weather": random.choice(["sunny", "cloudy", "rainy"])
    }

# --- Dashboard & AI APIs ---
@app.route('/api/solar-data', methods=['GET'])
def solar_data():
    return jsonify(generate_data())

@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    current_data = generate_data()
    suggestion = generate_suggestion(current_data)
    return jsonify({
        "data": current_data,
        "suggestion": suggestion
    })

# --- Emergency Page ---
@app.route('/api/emergency', methods=['GET'])
def emergency():
    return jsonify({
        "status": "Emergency Triggered",
        "type": "Battery Overload",
        "level": "High"
    })

# --- Analytics Page ---
@app.route('/api/analytics', methods=['GET'])
def analytics():
    return jsonify({
        "peak_hours": [1.2, 2.8, 3.6, 2.2, 0.5],
        "distribution": {
            "home": 42,
            "battery": 33,
            "grid": 25
        },
        "forecast": [12.5, 15.2, 13.1, 12.8, 14.9, 16.3, 17.1],
        "confidence": [2, 2.5, 1.8, 2, 2.2, 1.9, 2],
        "ai_info": {
            "accuracy": "94.7%",
            "data_points": 12458,
            "last_trained": "2 days ago",
            "next_update": "Tomorrow"
        }
    })

# --- Maintenance Page ---
@app.route('/api/maintenance', methods=['GET'])
def get_maintenance_data():
    return jsonify({
        "chart": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            "efficiency": [88, 85, 82, 90, 93, 89, 86],
            "cleaning_dates": [None, 90, None, None, 93, None, 86]
        }
    })

@app.route('/api/maintenance-history', methods=['GET'])
def maintenance_history():
    return jsonify([
        {"date": "2023-05-15", "task": "Panel Cleaning", "type": "Routine", "status": "Completed", "technician": "SolarCare Pro"},
        {"date": "2023-04-02", "task": "System Inspection", "type": "Quarterly", "status": "Completed", "technician": "SolarCare Pro"},
        {"date": "2023-03-10", "task": "Firmware Update", "type": "Software", "status": "Completed", "technician": "Remote"},
        {"date": "2023-02-28", "task": "Inverter Maintenance", "type": "Preventive", "status": "Completed", "technician": "SolarCare Pro"}
    ])

@app.route('/api/schedule-task', methods=['POST'])
def schedule_task():
    return jsonify({"message": "Task has been scheduled successfully!"})

@app.route('/api/task-info', methods=['POST'])
def task_info():
    return jsonify({"message": "Detailed task information retrieved."})

@app.route('/api/update-firmware', methods=['POST'])
def update_firmware():
    return jsonify({"message": "Firmware update completed."})

@app.route('/api/release-notes', methods=['GET'])
def release_notes():
    return jsonify({
        "notes": "Version 2.3.5: Improved performance, enhanced grid synchronization, and reduced latency in monitoring."
    })

# --- SETTINGS PAGE API ---

# Language dictionary (sample only)
translations = {
    "es": {"Dashboard": "Tablero", "Settings": "Configuración"},
    "fr": {"Dashboard": "Tableau de bord", "Settings": "Paramètres"},
    "de": {"Dashboard": "Armaturenbrett", "Settings": "Einstellungen"}
}

@app.route('/api/settings/preferences', methods=['POST'])
def save_preferences():
    data = request.get_json()
    print("Received Preferences:", data)
    return jsonify({"message": "Preferences saved successfully!"})

@app.route('/api/settings/reset', methods=['POST'])
def reset_preferences():
    return jsonify({"message": "Preferences reset to default"})

@app.route('/api/settings/config', methods=['POST'])
def system_config():
    data = request.get_json()
    print("System Config Changed:", data)
    return jsonify({"message": "System configuration updated"})

@app.route('/api/settings/security', methods=['POST'])
def update_password():
    data = request.get_json()
    if data.get("new_password") == data.get("confirm_password"):
        return jsonify({"message": "Password updated"})
    else:
        return jsonify({"message": "Passwords do not match"}), 400

@app.route('/api/settings/2fa', methods=['POST'])
def setup_2fa():
    data = request.get_json()
    number = data.get("mobile")
    return jsonify({"message": f"OTP sent to {number}", "otp": "123456"})  # Dummy OTP

@app.route('/api/settings/alerts', methods=['POST'])
def alert_settings():
    data = request.get_json()
    alert_type = data.get("type", "system")
    if "email" in data:
        try:
            msg = EmailMessage()
            msg.set_content("SolarSense Alert Triggered: " + alert_type)
            msg['Subject'] = 'SolarSense Alert Notification'
            msg['From'] = "yourmail@gmail.com"
            msg['To'] = data["email"]

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("yourmail@gmail.com", "yourapppassword")  # Replace with app password
                smtp.send_message(msg)
            return jsonify({"message": f"{alert_type.capitalize()} email sent"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Alert preference updated"})

# ✅ Chatbot route should go here, NOT inside the above function
import datetime
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_query = request.json.get("message", "").lower()

    # Get real-time solar data
    solar = generate_data()
    battery = solar["battery"]
    co2 = solar["co2_saved"]

    # Responses
    if "usage" in user_query and "solar" in user_query:
        reply = f"You can monitor your daily solar usage from the dashboard. Currently, it's {solar['usage']} kWh."

    elif "co2" in user_query or "carbon" in user_query:
        reply = f"The CO2 saved today is {co2} kg. 🌱"

    elif any(keyword in user_query for keyword in ["battery", "battery level", "battery percentage", "how much battery", "power stored"]):
        reply = f"The current battery level is {battery}%. 🔋"

    elif any(greet in user_query for greet in ["hello", "hi", "hey"]):
        reply = "Hello! I'm your Solar Sense assistant. Ask me anything!"

    else:
        reply = "I'm still learning. Please ask about solar usage, battery, CO2, or impact."

    # Log the chat
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user_query}\nBot: {reply}\n\n")

    return jsonify({"reply": reply})



# --- Start Server ---
if __name__ == '__main__':
    app.run(debug=True)

