from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8080"
)

@app.route("/orders")
def get_orders():
    response = requests.get(
        f"{BACKEND_URL}/orders",
        timeout=5
    )
    response.raise_for_status()

    return jsonify({
        "service": "frontend",
        "backend_response": response.json()
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
