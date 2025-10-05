from flask import Flask, jsonify
import json
from pathlib import Path
import os

app = Flask(__name__)


@app.route("/data")
def get_data():
    # Resolve processed_data.json relative to this backend module so the
    # server works regardless of current working directory.
    base_dir = Path(os.path.dirname(__file__))
    file_path = base_dir.joinpath("processed_data.json")

    if not file_path.exists():
        return jsonify({"error": f"{file_path} not found"}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "processed_data.json is malformed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(data)


@app.route("/")
def home():
    return {"message": "Backend API is running 🚀"}


if __name__ == "__main__":
    # Use 0.0.0.0 when you want to access from other machines, keep 127.0.0.1 for local dev
    app.run(debug=True, port=5000)
