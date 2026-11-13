import os
from google import genai
from flask import Flask, request, jsonify, send_from_directory, redirect, abort
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')

API_KEY = os.getenv("GEMINI_API_KEY")

BLOCKED_FILES = {'app.py', 'requirements.txt', 'vercel.json', 'cname', 'readme.md'}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
@app.route('/in1000')
@app.route('/in1000/')
@app.route('/python')
@app.route('/python/')
def redirect_in1000():
    return redirect('/', code=301)

@app.route('/in1010')
@app.route('/in1010/')
@app.route('/java')
@app.route('/java/')
def redirect_in1010():
    return redirect('/java.html', code=301)

@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')

@app.route('/<path:path>')
def serve_static(path):
    parts = path.split('/')
    lower_path = path.lower()
    if any(part.startswith('.') for part in parts) or lower_path.endswith('.py') or lower_path in BLOCKED_FILES:
        abort(404)
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
