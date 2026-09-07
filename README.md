# 🎙️ VoiceGuard AI — Real-Time AI Voice Clone Detection

> **Smart India Hackathon 2026 | Team ID: SIH26104**

Live Demo: [https://permalink-alumni-editorial-idea.trycloudflare.com](https://permalink-alumni-editorial-idea.trycloudflare.com)

---

## What It Does

VoiceGuard AI detects whether a voice is **real human** or **AI-generated clone** in under 2 seconds.

It protects people from:
- 📞 **Phone scams** — fake child/relative voice demanding money
- 🏦 **Bank fraud** — cloned CEO voice authorizing wire transfers
- 🎙️ **Deepfake audio** — fabricated politician/celebrity clips
- 👮 **Identity theft** — bypassing voice authentication systems

---

## How It Works

```
Audio Input
    ↓
Feature Extraction (librosa)
    ├── MFCC × 40 features     — vocal tract shape fingerprint
    ├── Pitch Variance (Hz)    — AI voices are unnaturally flat (5–15 Hz vs 30–80 Hz human)
    ├── RMS Dynamics           — AI volume is robotic-steady; humans breathe and stress
    ├── Spectral Flatness      — AI synthesis creates unnatural noise-floor patterns
    └── Zero Crossing Rate, Chroma, Delta-MFCC...  (66 features total)
    ↓
Logistic Regression Classifier (scikit-learn)
    ↓
REAL ✅  or  FAKE 🚨  + Confidence % + Acoustic Radar Chart
```

**Key Insight:** ElevenLabs AI pitch variance: ~5–15 Hz. Real humans: ~30–80 Hz. The model exploits this fundamental physical gap.

---

## Features

| Mode | Description |
|------|-------------|
| 🎤 **Live Microphone** | Speak for 5s → instant REAL/FAKE verdict |
| 📁 **File Upload** | Upload MP3/WAV/OGG/M4A for full analysis |
| 🤖 **Scam Simulator** | Generates real ElevenLabs AI voice → catches it live |
| ✓ **Voice Enrollment** | Record your own voice to improve model accuracy |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10 + Flask |
| ML / Audio | scikit-learn · librosa · numpy · soundfile |
| AI Voice Synthesis | ElevenLabs REST API |
| Frontend | Vanilla JS · Chart.js · Web Audio API |
| Database | SQLite |
| Hosting | Cloudflare Tunnel |

---

## Model Performance

- **Test Accuracy:** 100% on held-out test set
- **5-Fold Cross-Validation:** 98% ± 4%
- **Training Data:** 51 samples — 11 real human voices + 40 ElevenLabs AI voices (with mic simulation augmentation)
- **Features:** 66 acoustic features per sample
- **Detection Speed:** < 2 seconds end-to-end

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your ElevenLabs API key
Create a `.env` file:
```
ELEVENLABS_API_KEY=your_key_here
```

### 3. Train the model
```bash
python train.py
```

### 4. Run the server
```bash
python app.py
```

Open `http://localhost:5000`

### 5. (Optional) Public URL via Cloudflare
```bash
./cloudflared.exe tunnel --url http://localhost:5000
```

---

## Project Structure

```
VoiceCloneDetection/
├── app.py              # Flask server + API routes
├── ml_core.py          # Feature extraction + ML prediction
├── train.py            # Model training script
├── augment_fakes.py    # Mic simulation data augmentation
├── database.py         # SQLite scan history
├── make_html.py        # Generates templates/index.html
├── dataset/
│   ├── real/           # Real human voice samples
│   └── fake/           # ElevenLabs AI voice samples
├── model/
│   └── voiceguard.pkl  # Trained Logistic Regression model
├── templates/
│   └── index.html      # Frontend UI
└── uploads/            # Temporary scan audio files
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scan-mic` | POST | Analyze live mic recording |
| `/api/scan-file` | POST | Analyze uploaded audio file |
| `/api/generate-and-analyze` | POST | ElevenLabs synthesis + detection |
| `/api/enroll-real-voice` | POST | Save real voice + retrain model |
| `/api/stats` | GET | Scan statistics |
| `/api/history` | GET | Recent scan history |

---

## Team

Built for **Smart India Hackathon 2026** | Problem ID: **SIH26104**

---

*Python · Flask · scikit-learn · librosa · ElevenLabs · Cloudflare*
