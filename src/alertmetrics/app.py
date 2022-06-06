from flask import Flask, render_template, request
import requests
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Summary, Gauge, Counter, make_wsgi_app, Info
import datetime

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics" : make_wsgi_app( )
})

counters = {
    "alertmetrics_positive" : Counter("positive_feedback", "Positive feedback on notifications", ["id", "category"]),
    "alertmetrics_negative" : Counter("negative_feedback", "Negative feedback on notifications", ["id", "category"])
}

info = Info("alertmetrics_feedback", "Alertmetrics info")

def process_feedback(id, category, vote):

    if vote == "positive":
        counters["alertmetrics_positive"].labels(id, category).inc(1)
    elif vote == "negative":
        counters["alertmetrics_negative"].labels(id, category).inc(1)

    info.info({
        "id" : id,
        "category" : category,
        "vote" : vote,
        "time" : datetime.datetime.now().isoformat()
    })

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