from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)  # ✅ allow Chrome extension + browser requests

API_KEY = "AIzaSyB8Sn0S6H5bFFNV4vuaygJcBFxbcU7AT3M"
FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

# ✅ Serve the HTML interface
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# ✅ Fact-check API endpoint
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

    try:
        response = requests.get(FACTCHECK_URL, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
