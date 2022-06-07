""" This file contains the code for the alertmetrics app."""

import datetime
from flask import Flask, render_template, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Counter, make_wsgi_app, Info

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

counters = {
    "alertmetrics_positive": Counter(
        "positive_feedback",
        "Positive feedback on notifications",
        ["id", "category"]
    ),
    "alertmetrics_negative": Counter(
        "negative_feedback",
        "Negative feedback on notifications",
        ["id", "category"]
    )
}

info = Info("alertmetrics_feedback", "Alertmetrics info")


def process_feedback(alert_id, category, vote):
    """ Process feedback on an alert. """
    if vote == "positive":
        counters["alertmetrics_positive"].labels(alert_id, category).inc(1)
    elif vote == "negative":
        counters["alertmetrics_negative"].labels(alert_id, category).inc(1)

    info.info({
        "id": alert_id,
        "category": category,
        "vote": vote,
        "time": datetime.datetime.now().isoformat()
    })


@app.route("/")
def hello_world():
    """ Return the index page. """
    return render_template("index.html")


@app.route("/vote", methods=["GET"])
def predict():
    """ Render the page displaying the cast vote. """
    category = request.args.get("category")
    alert_id = request.args.get("id")
    vote = request.args.get("vote")

    process_feedback(alert_id, category, vote)
    return render_template("vote.html", category=category,
                           alert_id=alert_id, vote=vote)
