from flask import Flask, render_template, request
import pickle
import numpy as np
import time
import sys

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Summary, Gauge, Counter, make_wsgi_app, Info

from common.preprocessing import preprocess_sentence
from common.predicting import predict

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

model_folder = "."
vectorizer = pickle.load(open(f"{model_folder}/vectorizer.pkl", "rb"))
model = pickle.load(open(f"{model_folder}/tfidf_model.pkl", "rb"))
tags = np.loadtxt(f"{model_folder}/tags.txt", dtype=str, delimiter="\n")

queries = Counter("inference_queries", "Total queries")
predictions_count = Counter("inference_predictions", "Predictions", ["label"])
inference_time = Summary("inference_time", "Time to predict tags")


@app.route("/", methods=["POST"])
def predict_question_tags():

    start_time = current_milli_time()

    question = request.form.get("question")
    if question is None:
        return "No question provided"

    # Preprocess the question
    processed = preprocess_sentence(question, vectorizer)
    # Predict the tags
    predicted = predict(processed, model, tags)

    for pred in predicted:
        predictions_count.labels(pred).inc(1)

    end_time = current_milli_time()
    inference_time.observe(end_time - start_time)
    queries.inc()

    return {"tags": predicted}


def current_milli_time():
    return round(time.time() * 1000)
