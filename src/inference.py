from flask import Flask, render_template, request
import pickle
import numpy as np

from common.preprocessing import preprocess_sentence
from common.predicting import predict

model_folder = "outputs/models"
tags_location = "outputs/processed_data/tags.txt"

vectorizer = pickle.load(open(f"{model_folder}/vectorizer.pkl", "rb"))
model = pickle.load(open(f"{model_folder}/tfidf_model.pkl", "rb"))
tags = np.loadtxt(tags_location, dtype=str, delimiter="\n")

app = Flask(__name__)

@app.route("/", methods=["POST"])
def predict_question_tags():
    question = request.form.get("question")
    if question is None:
        return "No question provided"
    
    # Preprocess the question
    processed = preprocess_sentence(question, vectorizer)
    # Predict the tags
    predicted = predict(processed, model, tags)
    return {"tags": predicted}
