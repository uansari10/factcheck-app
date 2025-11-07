from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # ✅ allow Chrome extension requests

API_KEY = "AIzaSyB8Sn0S6H5bFFNV4vuaygJcBFxbcU7AT3M"
FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    query = data.get("query", "").strip()
    url = data.get("url", "").strip()

    if not query and not url:
        return jsonify({"error": "Must provide either 'query' or 'url'"}), 400

    params = {"key": API_KEY}
    if query:
        params["query"] = query
    if url:
        params["url"] = url

    response = requests.get(FACTCHECK_URL, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
