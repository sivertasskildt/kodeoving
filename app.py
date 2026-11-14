from collections import defaultdict, deque
import os
import threading
import time
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, redirect, abort
from google import genai
from google.genai import types
from werkzeug.exceptions import RequestEntityTooLarge

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

API_KEY = os.getenv("GEMINI_API_KEY")

BLOCKED_FILES = {'app.py', 'requirements.txt', 'vercel.json', 'cname', 'readme.md', 'license'}
ALLOWED_STATIC_HOSTS = {'kode.sask.no', 'www.kode.sask.no', 'localhost', '127.0.0.1', '::1'}
RATE_LIMIT_MINUTE = 20
RATE_LIMIT_HOUR = 120
MAX_CHAT_TURNS = 40
MAX_TOTAL_CHARS = 24000
MAX_OUTPUT_TOKENS = 4096

_rate_lock = threading.Lock()
_request_timestamps = defaultdict(deque)


def _get_client_ip():
    """Return the originating client IP address from headers or socket."""
    forwarded = request.headers.get('X-Forwarded-For', '')
    if forwarded:
        first_ip = forwarded.split(',')[0].strip()
        if first_ip:
            return first_ip
    return request.remote_addr or 'unknown'


def _is_rate_limited(client_ip):
    """Enforce sliding-window minute and hour limits per IP address."""
    now = time.monotonic()
    hour_cutoff = now - 3600
    minute_cutoff = now - 60

    with _rate_lock:
        if len(_request_timestamps) > 1000:
            stale_ips = [
                ip for ip, stamps in _request_timestamps.items()
                if not stamps or stamps[-1] <= hour_cutoff
            ]
            for ip in stale_ips:
                del _request_timestamps[ip]

        stamps = _request_timestamps[client_ip]
        while stamps and stamps[0] <= hour_cutoff:
            stamps.popleft()

        if len(stamps) >= RATE_LIMIT_HOUR:
            retry_after = max(1, int(3600 - (now - stamps[0])) + 1)
            return True, retry_after

        recent_minute = [t for t in stamps if t > minute_cutoff]
        if len(recent_minute) >= RATE_LIMIT_MINUTE:
            retry_after = max(1, int(60 - (now - recent_minute[0])) + 1)
            return True, retry_after

        stamps.append(now)
    return False, 0


def _is_allowed_origin():
    """Verify Origin/Referer matches this app in production."""
    source_header = request.headers.get('Origin') or request.headers.get('Referer')
    if not source_header:
        return bool(app.debug or app.testing)

    parsed = urlparse(source_header)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc:
        return False

    request_hosts = {request.host.lower()}
    forwarded_host = request.headers.get('X-Forwarded-Host', '').split(',')[0].strip().lower()
    if forwarded_host:
        request_hosts.add(forwarded_host)

    return (
        parsed.netloc.lower() in request_hosts
        or (parsed.hostname or '').lower() in ALLOWED_STATIC_HOSTS
    )


def _validate_contents(contents):
    """Validate text-only prompt/history shape and enforce character bounds."""
    if isinstance(contents, str):
        if not contents.strip():
            return "No contents provided"
        if len(contents) > MAX_TOTAL_CHARS:
            return "Input exceeds maximum allowed length"
        return None

    if not isinstance(contents, list) or not contents:
        return "Invalid contents format"
    if len(contents) > MAX_CHAT_TURNS:
        return "Conversation history exceeds maximum turns"

    total_chars = 0
    for turn in contents:
        if not isinstance(turn, dict):
            return "Invalid message turn format"
        role = turn.get('role')
        if role is not None and role not in ('user', 'model'):
            return "Invalid message role"
        parts = turn.get('parts')
        if not isinstance(parts, list) or not parts:
            return "Invalid message parts"
        for part in parts:
            if not isinstance(part, dict) or set(part.keys()) != {'text'}:
                return "Only text message parts are allowed"
            text = part.get('text')
            if not isinstance(text, str) or not text.strip():
                return "Message text must be a non-empty string"
            total_chars += len(text)
            if total_chars > MAX_TOTAL_CHARS:
                return "Input exceeds maximum allowed length"

    return None


@app.errorhandler(RequestEntityTooLarge)
def handle_payload_too_large(_error):
    return jsonify({"error": "Forespørselen er for stor."}), 413

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
    if not _is_allowed_origin():
        return jsonify({"error": "Ugyldig opprinnelse for forespørselen."}), 403

    limited, retry_after = _is_rate_limited(_get_client_ip())
    if limited:
        response = jsonify({"error": "For mange forespørsler. Vent litt før du prøver igjen."})
        response.status_code = 429
        response.headers['Retry-After'] = str(retry_after)
        return response

    if not API_KEY:
        return jsonify({"error": "Server configuration error: API Key missing"}), 500

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    contents = data.get('contents')
    validation_error = _validate_contents(contents)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-4-hydrogen",
            contents=contents,
            config=types.GenerateContentConfig(max_output_tokens=MAX_OUTPUT_TOKENS)
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
