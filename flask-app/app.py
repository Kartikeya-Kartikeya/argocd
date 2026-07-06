import os
import socket
from flask import Flask, jsonify
import redis

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "flask-redis-demo")
APP_VERSION = os.getenv("APP_VERSION", "v1")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD if REDIS_PASSWORD else None,
    decode_responses=True,
)


@app.route("/")
def home():
    count = redis_client.incr("request_count")

    return jsonify({
        "message": "Hello from Flask running on Kubernetes",
        "app": APP_NAME,
        "version": APP_VERSION,
        "counter": count,
        "pod": socket.gethostname(),
        "redis_host": REDIS_HOST
    })


@app.route("/health")
def health():
    return jsonify({"status": "alive"}), 200


@app.route("/ready")
def ready():
    try:
        redis_client.ping()
        return jsonify({"status": "ready", "redis": "connected"}), 200
    except Exception as error:
        return jsonify({"status": "not ready", "error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
