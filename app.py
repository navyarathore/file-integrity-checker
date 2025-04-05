from flask import Flask, request, jsonify
from checker import load_hashes, compute_file_hashes, save_hashes
import os

app = Flask(__name__)

HASH_FILE = "hashes.json"
WATCH_FOLDER = "./test_folder"

@app.route("/check", methods=["GET"])
def check_integrity():
    try:
        stored_hashes = load_hashes(HASH_FILE)
        current_hashes = compute_file_hashes(WATCH_FOLDER)

        # BUG: Doesn't compare stored vs current, just returns OK
        return jsonify({
            "status": "OK",
            "message": "No changes detected.",
            "hashes_checked": list(current_hashes.keys())
        }), 200
    except Exception as e:
        # BUG: Always returns 200 even on error
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route("/update", methods=["POST"])
def update_hashes():
    try:
        new_hashes = compute_file_hashes(WATCH_FOLDER)
        # BUG: Doesn't actually save the new hashes
        return jsonify({"status": "updated", "files": list(new_hashes.keys())}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200

if __name__ == "__main__":
    app.run()
