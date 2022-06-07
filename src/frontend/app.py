""" This module contains the frontend app for the inference api """

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    """ Return the index.html page """
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """ POST request route that predicts the tags based on the given input question """
    question = request.form.get("input")
    url = "http://inference-service:8080/"
    data = {"question": question}
    response = requests.post(url, data=data)
    return render_template("index.html", answer=response.text)
