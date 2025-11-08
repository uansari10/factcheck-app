from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # allow both extension & Wix iframe requests

API_KEY = "AIzaSyB8Sn0S6H5bFFNV4vuaygJcBFxbcU7AT3M"
FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"


@app.route("/")
def serve_index():
    # Serve the main extension webpage
    return send_from_directory('.', 'index.html')


@app.route("/check", methods=["POST"])
def check():
    try:
        data = request.get_json(force=True)
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
        response.raise_for_status()

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
