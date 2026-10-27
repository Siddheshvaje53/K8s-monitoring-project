from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time, random

app = Flask(__name__)

REQUESTS = Counter("app_requests_total", "Total requests", ["endpoint"])
LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])

@app.route("/")
def home():
    start = time.time()
    REQUESTS.labels("/").inc()
    time.sleep(random.uniform(0.01, 0.2)) # simulate work
    LATENCY.labels("/").observe(time.time() - start)
    return "Hello from my kubernetes app"

@app.route("/health")
def health():
    return "OK"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type" : CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)