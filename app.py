from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LibreTranslate public server
LIBRE_URL = "https://libretranslate.com/translate"

@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        text = data.get("text")
        source = data.get("source", "auto")  # default: auto-detect
        target = data.get("target", "en")    # default: English

        if not text:
            return jsonify({"error": "No text provided"}), 400

        payload = {
            "q": text,
            "source": source,
            "target": target,
            "format": "text"
        }

        # Call LibreTranslate
        response = requests.post(LIBRE_URL, json=payload, timeout=10)

        # Debugging: print full response
        print("LibreTranslate response:", response.text)

        # Check if response is OK
        if response.status_code != 200:
            return jsonify({"error": "LibreTranslate error", "details": response.text}), 500

        translated_text = response.json().get("translatedText", "")
        return jsonify({"translatedText": translated_text})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    print("Starting API... visit http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
