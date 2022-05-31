from flask import Flask, render_template, request
import requests

app = Flask(__name__)

feedback = {}

def process_feedback(id, category, vote):
    if id not in feedback:
        feedback[id] = {
            "category": category,
            "positive": 1 if vote == "positive" else 0,
            "negative": 1 if vote == "negative" else 0
        }
    else:
        feedback[id]["positive"] += 1 if vote == "positive" else 0
        feedback[id]["negative"] += 1 if vote == "negative" else 0

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/vote", methods=["GET"])
def predict():
    category = request.args.get("category")
    alert_id = request.args.get("id")
    vote = request.args.get("vote")

    process_feedback(alert_id, category, vote)
    return render_template("vote.html", category=category, alert_id=alert_id, vote=vote)

@app.route('/metrics')
def metrics():
    metrics = ""
    positive_votes = 0
    negative_votes = 0
    for id in feedback:
        positive_votes += feedback[id]["positive"]
        negative_votes += feedback[id]["negative"]
        metrics += f'alertmetrics_predicted_total{{category="{feedback[id]["category"]}",positive="{feedback[id]["positive"]}",negative="{feedback[id]["negative"]}"}} 1\n'
    
    metrics += f'alertmetrics_positive_votes {positive_votes}\n'
    metrics += f'alertmetrics_negative_votes {negative_votes}\n'

    return metrics