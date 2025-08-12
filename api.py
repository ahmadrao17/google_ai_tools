# api.py

from flask import Flask, request, jsonify, send_file
import asyncio
from test_generater import testGenerator
import requests

app = Flask(__name__)

@app.route('/test-generator', methods=["POST"])
def test_generator():
    data = request.get_json()
    if not data or "filename" not in data or "file_base64" not in data:
        return jsonify({"error": "Missing filename or file_base64"}), 400
    result = testGenerator(data)
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
