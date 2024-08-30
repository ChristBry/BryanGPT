from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import re

app = Flask(__name__)

# Remplacez par votre token Hugging Face
client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token="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",
)

def clean_response(text):
    # Supprimer les blocs de code
    text = remove_code_blocks(text)
    # Supprimer les motifs spécifiques
    patterns = [r'^\s*Note:', r'^\s*Disclaimer:', r'^\s*Warning:']
    text = remove_patterns(text, patterns)
    # Tronquer si trop long
    text = truncate_text(text, 400)
    # Supprimer les caractères spéciaux
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def remove_code_blocks(text):
    # Supprimer les blocs de code formatés par des backticks
    return re.sub(r'```.*?```', '', text, flags=re.DOTALL)

def remove_patterns(text, patterns):
    # Supprimer les motifs spécifiques
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return text

def truncate_text(text, max_length):
    # Tronquer le texte s'il dépasse la longueur maximale
    return text if len(text) <= max_length else text[:max_length] + '...'

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", response="")

@app.route("/api", methods=["POST"])
def api():
    if request.method == "POST":
        data = request.form  # Pour recevoir des données envoyées avec "application/x-www-form-urlencoded"
        user_input = data['user_input']  # Récupère le message de l'utilisateur

        # Appel à l'API Hugging Face
        messages = [{"role": "user", "content": user_input}]
        response = ""

        # Traitement en streaming pour obtenir la réponse
        for message in client.chat_completion(
            messages=messages,
            max_tokens=500,
            stream=True,
        ):
            response += message.choices[0].delta.content

        # Retourne la réponse sous forme de JSON
        return jsonify({"content": response})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)