""" The inference application provides access to the model
    through an HTTP API served by Flask. """

import pickle
import time
from flask import Flask, request
import numpy as np
from prometheus_client import Summary, Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from common.preprocessing import preprocess_sentence
from common.predicting import predict

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

# pylint: disable=consider-using-with
MODEL_FOLDER = "."
vectorizer = pickle.load(open(f"{MODEL_FOLDER}/vectorizer.pkl", "rb"))
model = pickle.load(open(f"{MODEL_FOLDER}/tfidf_model.pkl", "rb"))
tags = np.loadtxt(f"{MODEL_FOLDER}/tags.txt", dtype=str, delimiter="\n")
# pylint: enable=consider-using-with

queries = Counter("inference_queries", "Total queries")
predictions_count = Counter("inference_predictions", "Predictions", ["label"])
inference_time = Summary("inference_time", "Time to predict tags")


@app.route("/", methods=["POST"])
def predict_question_tags():
    """ Flask controller performing model inference. """
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
    """ Returns current time in milliseconds. """
    return round(time.time() * 1000)
