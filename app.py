"""
VoiceGuard - Flask Backend
"""

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import time
import logging
import requests
import werkzeug.utils
from flask import Flask, request, jsonify, render_template, send_from_directory
from ml_core import VoiceGuardDetector
from database import init_db, log_scan, get_recent_scans, get_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]        = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"]   = 50 * 1024 * 1024   # 50 MB

# ElevenLabs config — set env var or hardcode for demo
ELEVENLABS_API_KEY  = os.getenv("ELEVENLABS_API_KEY", "sk_e965d7392f9bed5d878fd846f79404a16d8c86270c8503a3")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "CwhRBWXzGAHq8TQ4Fs17")   # Roger - works on free plan

os.makedirs(app.config["UPLOAD_FOLDER"],                        exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "dataset", "real"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "dataset", "fake"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "model"),           exist_ok=True)

# -- Startup --
init_db()
print("[VoiceGuard] Initialising...")
detector = VoiceGuardDetector()
if detector.model_loaded:
    print("[VoiceGuard] Custom Random Forest model active")
else:
    print("[VoiceGuard] No trained model found - running in heuristic mode")
    print("             Run  python train.py  to activate the full model")
print("[VoiceGuard] Server starting on http://127.0.0.1:5000\n")


# ── Helper ───────────────────────────────────────────────────────────────────
def _save_upload(file, prefix="upload") -> tuple[str, str]:
    """Securely save an uploaded file. Returns (safe_filename, filepath)."""
    original = werkzeug.utils.secure_filename(file.filename or "recording.webm")
    filename  = f"{prefix}_{int(time.time())}_{original}"
    filepath  = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    return filename, filepath


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({
        "model_loaded": detector.model_loaded,
        "elevenlabs_configured": bool(ELEVENLABS_API_KEY),
        "version": "1.0.0",
    })


@app.route("/api/scan-file", methods=["POST"])
def scan_file():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    filename, filepath = _save_upload(file)
    result = detector.predict(filepath)

    log_scan(
        filename=file.filename,
        status=result["status"],
        confidence=result["confidence"],
        features=result["features"],
        source="file_upload",
    )

    result["filename"]  = file.filename
    result["audio_url"] = f"/uploads/{filename}"
    return jsonify(result)


@app.route("/api/scan-mic", methods=["POST"])
def scan_mic():
    if "audio" not in request.files:
        return jsonify({"error": "No audio provided"}), 400

    file = request.files["audio"]
    filename, filepath = _save_upload(file, prefix="mic")
    result = detector.predict(filepath)

    log_scan(
        filename="Live Recording",
        status=result["status"],
        confidence=result["confidence"],
        features=result["features"],
        source="live_mic",
    )

    result["filename"]  = "Live Recording"
    result["audio_url"] = f"/uploads/{filename}"
    return jsonify(result)


@app.route("/api/generate-and-analyze", methods=["POST"])
def generate_and_analyze():
    """Generate a fake voice via ElevenLabs, then immediately analyze it."""
    if not ELEVENLABS_API_KEY:
        return jsonify({
            "error": (
                "ElevenLabs API key not set. "
                "Add ELEVENLABS_API_KEY to your environment or set it in app.py."
            )
        }), 400

    data  = request.get_json(silent=True) or {}
    text  = data.get("text", "Namaste, aapka bank account band hone wala hai.").strip()

    if not text:
        return jsonify({"error": "Text is empty"}), 400

    # Call ElevenLabs
    url     = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        # Free plan fallback to flash model
        if resp.status_code == 402:
            payload["model_id"] = "eleven_flash_v2_5"
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            return jsonify({"error": f"ElevenLabs error {resp.status_code}: {resp.text[:120]}"}), 500
    except requests.RequestException as e:
        return jsonify({"error": f"Network error: {e}"}), 500

    # Save generated audio
    ts       = int(time.time())
    filename = f"sim_{ts}.mp3"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with open(filepath, "wb") as f:
        f.write(resp.content)

    # Analyze
    result = detector.predict(filepath)

    log_scan(
        filename=f"Simulator: {text[:40]}",
        status=result["status"],
        confidence=result["confidence"],
        features=result["features"],
        source="scam_simulator",
    )

    result["audio_url"]      = f"/uploads/{filename}"
    result["generated_text"] = text
    return jsonify(result)


@app.route("/api/history")
def history():
    limit = min(int(request.args.get("limit", 20)), 100)
    return jsonify(get_recent_scans(limit=limit))


@app.route("/api/stats")
def stats():
    return jsonify(get_stats())


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# -- Entry point --
if __name__ == "__main__":
    app.run(debug=False, port=5000, threaded=True, use_reloader=False)
