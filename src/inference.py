from flask import Flask, render_template, request
import pickle
import numpy as np
import sys

from common.preprocessing import preprocess_sentence
from common.predicting import predict

app = Flask(__name__)
tag_predictions = {}


@app.route("/", methods=["POST"])
def predict_question_tags():
    print(request.data)
    question = request.form.get("question")
    if question is None:
        return "No question provided"
    
    # Preprocess the question
    processed = preprocess_sentence(question, vectorizer)
    # Predict the tags
    predicted = predict(processed, model, tags)

    for pred in predicted:
        tag_predictions[pred] = 1 if pred not in tag_predictions else tag_predictions[pred] + 1

    return {"tags": predicted}

@app.route('/metrics')
def metrics():
    metrics = ""
    for tag in tag_predictions:
        metrics += f'predicted_total{{tag="{tag}"}} {tag_predictions[tag]}\n'

    return metrics


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inference_api.py [model_folder]")
        exit(1)
    model_folder = sys.argv[1]

    vectorizer = pickle.load(open(f"{model_folder}/vectorizer.pkl", "rb"))
    model = pickle.load(open(f"{model_folder}/tfidf_model.pkl", "rb"))
    tags = np.loadtxt(f"{model_folder}/tags.txt", dtype=str, delimiter="\n")
