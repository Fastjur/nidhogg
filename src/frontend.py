from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    question = request.form.get("input")
    url = "http://inference-service:8080/"
    data = {"question": question}
    response = requests.post(url, data=data, headers={"Content-Type": "form-data"})
    return render_template("index.html", answer=response.text)