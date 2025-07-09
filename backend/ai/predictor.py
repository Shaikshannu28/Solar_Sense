def generate_suggestion(data):
    generation = data["generation"]
    usage = data["usage"]
    battery = data["battery"]
    weather = data["weather"]

    if generation < 2.0:
        return "⚠️ Low solar generation. Conserve or switch to battery."
    elif battery < 60:
        return "🔋 Battery level is low. Limit heavy usage."
    elif weather == "cloudy":
        return "🌥️ Cloudy forecast. Solar efficiency may drop."
    elif usage > generation:
        return "⚡ Usage is higher than generation. Monitor usage."
    else:
        return "✅ System optimal. You can use solar freely."
