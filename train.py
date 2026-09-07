"""
VoiceGuard -- Training Script
1. Put real voice clips  in  dataset/real/
2. Put fake voice clips  in  dataset/fake/
3. Run:  python train.py
"""

import os
import sys
import pickle
import warnings
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(__file__))
from ml_core import extract_features

DATASET_REAL = os.path.join(os.path.dirname(__file__), "dataset", "real")
DATASET_FAKE = os.path.join(os.path.dirname(__file__), "dataset", "fake")
MODEL_DIR    = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH   = os.path.join(MODEL_DIR, "voiceguard.pkl")

FORMATS = (".wav", ".mp3", ".ogg", ".m4a", ".flac", ".webm", ".aac", ".mp4", ".mpeg")


def load_dataset():
    X, y = [], []

    print("\n" + "=" * 52)
    print("   VoiceGuard -- Dataset Loading")
    print("=" * 52)

    def load_dir(directory, label, label_name):
        count = 0
        if not os.path.isdir(directory):
            print(f"\n  [!] Folder not found: {directory}")
            return 0
        files = [f for f in sorted(os.listdir(directory))
                 if f.lower().endswith(FORMATS)]
        print(f"\n  [{label_name}] ({len(files)} files) -- {directory}")
        for fname in files:
            fpath = os.path.join(directory, fname)
            try:
                feats, _ = extract_features(fpath)
                X.append(feats)
                y.append(label)
                count += 1
                print(f"     OK  {fname}")
            except Exception as e:
                print(f"     ERR {fname}: {e}")
        return count

    real_n = load_dir(DATASET_REAL, 0, "REAL voices")
    fake_n = load_dir(DATASET_FAKE, 1, "FAKE voices")

    print(f"\n  Dataset summary:")
    print(f"    Real  : {real_n}")
    print(f"    Fake  : {fake_n}")
    print(f"    Total : {real_n + fake_n}")

    if real_n == 0 or fake_n == 0:
        print("\n  ERROR: Need samples in both classes. Check dataset folders.")
        sys.exit(1)

    if real_n < 10 or fake_n < 10:
        print("\n  WARNING: Small dataset. Aim for 20+ per class for better accuracy.")

    return np.array(X), np.array(y)


def train():
    X, y = load_dataset()

    print("\n" + "=" * 52)
    print("   Training Model")
    print("=" * 52)

    test_size = 0.2 if len(X) >= 20 else 0.15
    try:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
    except ValueError:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

    print(f"\n  Train: {len(X_tr)}  |  Test: {len(X_te)}")
    print("\n  Training... (under 15 seconds)")

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            class_weight='balanced',
            C=0.5,
            max_iter=1000,
            random_state=42
        ))
    ])

    pipeline.fit(X_tr, y_tr)

    y_pred = pipeline.predict(X_te)
    acc    = accuracy_score(y_te, y_pred)

    print(f"\n  Done!")
    print(f"\n  Test Accuracy : {acc * 100:.1f}%")

    if len(set(y_te)) > 1:
        print("\n" + classification_report(y_te, y_pred, target_names=["REAL", "FAKE"]))

    n_cv = min(5, len(X) // 4)
    if n_cv >= 2:
        cv = cross_val_score(pipeline, X, y, cv=n_cv, scoring="accuracy")
        print(f"  Cross-val ({n_cv}-fold): {cv.mean()*100:.1f}% +/- {cv.std()*100:.1f}%")

    if acc < 0.70:
        print("\n  WARNING: Accuracy below 70%. Add more diverse training samples.")

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    print(f"\n  Model saved -> {MODEL_PATH}")
    print("\n  Now run:  python app.py")
    print("=" * 52 + "\n")


if __name__ == "__main__":
    train()
