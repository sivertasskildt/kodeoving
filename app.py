import os
from google import genai
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/generate', methods=['POST'])
def generate():
    if not API_KEY:
        return jsonify({"error": "Server configuration error: API Key missing"}), 500

    data = request.json
    contents = data.get('contents')

    if not contents:
        return jsonify({"error": "No contents provided"}), 400

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=contents
        )
        return jsonify({
            "candidates": [{
                "content": {
                    "parts": [{"text": response.text}]
                }
            }]
        })
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Failed to communicate with AI service"}), 502

if __name__ == '__main__':
    print("Starting server on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
