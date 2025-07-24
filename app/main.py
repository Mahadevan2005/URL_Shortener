from flask import Flask, request, jsonify, redirect
from app.models import URLStore
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)
store = URLStore()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    url = data['url']
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while store.get(short_code):  # avoid collision
        short_code = generate_short_code()

    store.save(short_code, url)

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>')
def redirect_short_url(short_code):
    data = store.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404

    store.increment_click(short_code)
    return redirect(data['url'])

@app.route('/api/stats/<short_code>')
def url_stats(short_code):
    data = store.stats(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": data['url'],
        "clicks": data['clicks'],
        "created_at": data['created_at']
    })
