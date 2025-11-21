from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from model import UTPAssistModel

import os
print("Current working directory:", os.getcwd())
print("Templates folder exists:", os.path.exists("templates"))

app = Flask(__name__)
CORS(app) 

try:
    bot = UTPAssistModel()
    print("Chatbot model loaded successfully.")
except FileNotFoundError:
    print("ERROR: UTP_Chatbot_Dataset.xlsx not found. Please ensure the dataset file is in the same directory.")
    bot = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    if not bot:
        return jsonify({"response": "The chatbot model failed to load (dataset missing). Check server logs."}), 500
    
    user_input = request.json.get("prompt")
    if not user_input:
        return jsonify({"response": "Please type a question."})
    
    response = bot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

