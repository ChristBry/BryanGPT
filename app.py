from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", response="")

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()  # Récupère les données JSON de la requête
    user_input = data['message']  # Récupère le message de l'utilisateur

    # Appel à l'API Hugging Face
    response = query({"inputs": user_input})
    bot_response = response[0]['generated_text']

    return jsonify({"content": bot_response})

if __name__ == "__main__":
    app.run(debug=True)