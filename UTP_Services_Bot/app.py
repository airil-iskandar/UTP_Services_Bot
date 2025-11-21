from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # New import for Cross-Origin Resource Sharing
from model import UTPAssistModel

import os
# Check current working directory for debugging purposes
print("Current working directory:", os.getcwd())
# Ensure the templates folder exists for Flask to find index.html
print("Templates folder exists:", os.path.exists("templates"))


# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes, allowing the frontend to connect
CORS(app) 

# Load the trained bot
# NOTE: This assumes 'UTP_Chatbot_Dataset.csv' is in the same directory as app.py and model.py
try:
    bot = UTPAssistModel() # Loads CSV dataset and prepares TF-IDF
    print("Chatbot model loaded successfully.")
except FileNotFoundError:
    print("ERROR: UTP_Chatbot_Dataset.csv not found. Please ensure the dataset file is in the same directory.")
    bot = None # Set bot to None if loading fails

# ---------------- Routes ----------------

# Main page (This assumes you will run Flask to serve the HTML file)
@app.route("/")
def index():
    # Flask looks for index.html inside a 'templates' folder.
    return render_template("index.html")

# Handle user questions from web (Frontend will call this endpoint)
@app.route("/ask", methods=["POST"])
def ask():
    if not bot:
        return jsonify({"response": "The chatbot model failed to load (dataset missing). Check server logs."}), 500

    user_input = request.json.get("prompt") # Changed from 'message' to 'prompt' to match the frontend JSON structure
    if not user_input:
        return jsonify({"response": "Please type a question."})

    response = bot.get_response(user_input)
    # The frontend expects the response key to be "response"
    return jsonify({"response": response})

# Run the app
if __name__ == "__main__":
    # Ensure you have 'Flask', 'flask_cors', 'pandas', and 'scikit-learn' installed.
    app.run(debug=True)