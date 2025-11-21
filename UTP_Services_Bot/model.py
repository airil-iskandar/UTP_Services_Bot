import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def preprocess(text):
    """Lowercase and remove punctuation"""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

class UTPAssistModel:
    def __init__(self, dataset_path="UTP_Chatbot_Dataset.csv"):
        # Load dataset with proper encoding
        self.df = pd.read_csv(dataset_path, encoding="cp1252")  # or "utf-8"

        # Preprocess questions
        self.df["processed_question"] = self.df["question"].astype(str).apply(preprocess)

        # Build TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.df["processed_question"])

    def get_response(self, user_input):
        # Preprocess user input
        user_input_processed = preprocess(user_input)

        # Transform user input
        user_vec = self.vectorizer.transform([user_input_processed])

        # Calculate similarity
        similarities = cosine_similarity(user_vec, self.question_vectors)[0]
        best_index = similarities.argmax()
        best_score = similarities[best_index]

        # Confidence threshold
        if best_score < 0.3:
            return "Sorry, I’m not sure about that. Try rephrasing your question."

        return self.df.iloc[best_index]["answer"]
