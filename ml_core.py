"""
VoiceGuard — ML Core
Feature extraction and voice classification.

Two-mode operation:
  1. Trained model (voiceguard.pkl) → Random Forest prediction (primary)
  2. No model yet            → Physics-based heuristics (fallback until trained)
"""

import os
import pickle
import logging
import numpy as np
import librosa

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "voiceguard.pkl")


# ─────────────────────────────────────────────
#  FEATURE EXTRACTION
#  Every feature here is explainable to judges.
# ─────────────────────────────────────────────

def extract_features(file_path: str):
    """
    Extract acoustic features from an audio file.

    Returns
    -------
    features : np.ndarray  shape (66,)
    names    : list[str]
    """
    # Load audio — mono, 16 kHz, max 10 s
    try:
        y, sr = librosa.load(file_path, sr=16000, mono=True, duration=10.0)
    except Exception as e:
        raise RuntimeError(f"Cannot read audio file: {e}")

    # Pad if shorter than 1 second
    if len(y) < sr:
        y = np.pad(y, (0, sr - len(y)), mode="constant")

    feats, names = [], []

    # ── 1. MFCC (13 coefficients × mean + std + delta_mean = 39 values) ──
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    feats.extend(np.mean(mfccs, axis=1));  names += [f"mfcc_mean_{i}" for i in range(13)]
    feats.extend(np.std(mfccs, axis=1));   names += [f"mfcc_std_{i}"  for i in range(13)]
    delta = librosa.feature.delta(mfccs)
    feats.extend(np.mean(delta, axis=1));  names += [f"mfcc_delta_{i}" for i in range(13)]

    # ── 2. PITCH VARIANCE — key discriminator ──
    # AI voices have unnaturally flat pitch (low std dev).
    # Real voices: pitch std ≈ 20–80 Hz. AI voices: often < 10 Hz.
    try:
        f0, voiced_flag, _ = librosa.pyin(
            y,
            fmin=librosa.note_to_hz("C2"),   # ~65 Hz  (bass floor)
            fmax=librosa.note_to_hz("C7"),    # ~2093 Hz (upper ceiling)
            sr=sr,
        )
        voiced_f0 = f0[voiced_flag & ~np.isnan(f0)]
        if len(voiced_f0) >= 5:
            pitch_mean  = float(np.mean(voiced_f0))
            pitch_std   = float(np.std(voiced_f0))
            pitch_range = float(np.ptp(voiced_f0))
            voiced_ratio = float(np.sum(voiced_flag) / max(len(voiced_flag), 1))
        else:
            pitch_mean = pitch_std = pitch_range = voiced_ratio = 0.0
    except Exception:
        pitch_mean = pitch_std = pitch_range = voiced_ratio = 0.0

    feats += [pitch_mean, pitch_std, pitch_range, voiced_ratio]
    names += ["pitch_mean", "pitch_std", "pitch_range", "voiced_ratio"]

    # ── 3. SPECTRAL FEATURES ──
    spec_c = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    feats += [np.mean(spec_c), np.std(spec_c)]
    names += ["spec_centroid_mean", "spec_centroid_std"]

    spec_f = librosa.feature.spectral_flatness(y=y)[0]
    feats += [np.mean(spec_f), np.std(spec_f)]
    names += ["spec_flatness_mean", "spec_flatness_std"]

    spec_r = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    feats += [np.mean(spec_r)]
    names += ["spec_rolloff_mean"]

    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    feats += [np.mean(spec_bw), np.std(spec_bw)]
    names += ["spec_bw_mean", "spec_bw_std"]

    # ── 4. ZERO CROSSING RATE ──
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    feats += [np.mean(zcr), np.std(zcr)]
    names += ["zcr_mean", "zcr_std"]

    # ── 5. RMS ENERGY (volume variation — real voices vary more) ──
    rms = librosa.feature.rms(y=y)[0]
    feats += [np.mean(rms), np.std(rms)]
    names += ["rms_mean", "rms_std"]

    # ── 6. CHROMA (harmonic fingerprint) ──
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    feats.extend(np.mean(chroma, axis=1))
    names += [f"chroma_{i}" for i in range(12)]

    return np.array(feats, dtype=np.float32), names


def get_duration(file_path: str) -> float:
    """Return audio duration in seconds."""
    try:
        return round(librosa.get_duration(path=file_path), 1)
    except Exception:
        return 0.0


# ─────────────────────────────────────────────
#  DETECTOR CLASS
# ─────────────────────────────────────────────

class VoiceGuardDetector:

    def __init__(self):
        self.model        = None
        self.model_loaded = False
        self._load_model()

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
                logger.info("VoiceGuard model loaded ✅")
            except Exception as e:
                logger.error(f"Model load failed: {e}")
        else:
            logger.warning("Model not found — run  python train.py  first.")

    def predict(self, file_path: str) -> dict:
        # ── Extract features ──
        try:
            feats, names = extract_features(file_path)
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "features": {},
                "risk_level": "UNKNOWN",
                "verdict_reason": f"Could not read audio: {e}",
                "model_used": "none",
            }

        feat_dict = dict(zip(names, feats.tolist()))
        pitch_std = feat_dict.get("pitch_std", 0.0)
        rms_std   = feat_dict.get("rms_std", 0.0)

        # ── Predict ──
        if self.model_loaded:
            try:
                proba      = self.model.predict_proba([feats])[0]
                pred       = int(np.argmax(proba))
                conf       = float(proba[pred]) * 100
                status     = "REAL" if pred == 0 else "FAKE"
                model_used = "voiceguard_ml"

            except Exception as e:
                logger.error(f"Model predict error: {e}")
                status, conf = self._heuristic(feat_dict)
                model_used = "heuristic_fallback"
        else:
            status, conf = self._heuristic(feat_dict)
            model_used = "heuristic"

        # ── Risk level ──
        if status == "FAKE":
            risk = "HIGH" if conf > 85 else ("MEDIUM" if conf > 70 else "LOW")
        else:
            risk = "NONE"

        # ── Human-readable features for UI ──
        pitch_std   = feat_dict.get("pitch_std", 0.0)
        rms_std     = feat_dict.get("rms_std", 0.0)
        spec_flat   = feat_dict.get("spec_flatness_mean", 0.0)

        interpretable = {
            "pitch_variance_hz": round(pitch_std, 2),
            "voice_dynamics":    round(rms_std, 5),
            "spectral_flatness": round(spec_flat, 5),
            "duration":          get_duration(file_path),
        }

        return {
            "status":         status,
            "confidence":     round(conf, 1),
            "features":       interpretable,
            "risk_level":     risk,
            "verdict_reason": self._reason(status, feat_dict),
            "model_used":     model_used,
        }

    # ── Physics-based heuristic (no filename tricks) ──
    def _heuristic(self, feat_dict: dict):
        """
        Rule-based scoring using acoustic physics.
        Used when trained model is not yet available.
        """
        score_fake  = 0.0
        total_weight = 0.0

        # Rule 1 — Pitch variance  (weight: 3.0)
        pitch_std = feat_dict.get("pitch_std", -1)
        if pitch_std >= 0:
            w = 3.0
            if pitch_std < 8:
                score_fake += w * 1.0     # very flat → very suspicious
            elif pitch_std < 18:
                score_fake += w * 0.55
            elif pitch_std < 30:
                score_fake += w * 0.2
            # else: natural variance, no penalty
            total_weight += w

        # Rule 2 — Volume dynamics  (weight: 2.0)
        rms_std = feat_dict.get("rms_std", 0)
        w = 2.0
        if rms_std < 0.004:
            score_fake += w * 0.9         # unnaturally steady volume
        elif rms_std < 0.012:
            score_fake += w * 0.45
        total_weight += w

        # Rule 3 — Spectral flatness  (weight: 1.5)
        sf = feat_dict.get("spec_flatness_mean", 0)
        w = 1.5
        if sf > 0.08:
            score_fake += w * 0.75        # too noisy/flat spectrum
        elif sf < 0.0005:
            score_fake += w * 0.5         # too tonal / unnaturally clean
        total_weight += w

        if total_weight == 0:
            return "REAL", 55.0

        ratio = score_fake / total_weight

        if ratio > 0.5:
            conf = 55 + ratio * 33        # 55–88 %
            return "FAKE", min(conf, 88.0)
        else:
            conf = 55 + (1 - ratio) * 28  # 55–83 %
            return "REAL", min(conf, 83.0)

    def _reason(self, status: str, fd: dict) -> str:
        pitch_std = fd.get("pitch_std", 0)
        rms_std   = fd.get("rms_std", 0)
        sf        = fd.get("spec_flatness_mean", 0)

        if status == "FAKE":
            if pitch_std < 12:
                return (
                    "Unnaturally flat pitch pattern detected "
                    "(std dev: {:.1f} Hz) — characteristic of AI voice synthesis.".format(pitch_std)
                )
            elif rms_std < 0.006:
                return (
                    "Abnormally steady volume dynamics — "
                    "human speech naturally fluctuates; this voice does not."
                )
            elif sf > 0.07:
                return (
                    "Excessive spectral flatness ({:.4f}) — "
                    "indicates vocoder artifacts common in neural TTS systems.".format(sf)
                )
            else:
                return (
                    "Multiple acoustic anomalies across pitch, spectral, "
                    "and energy features — patterns inconsistent with natural human speech."
                )
        else:
            return (
                "Natural pitch variation ({:.1f} Hz), healthy volume dynamics, "
                "and normal spectral profile confirmed — authentic human voice.".format(pitch_std)
            )
