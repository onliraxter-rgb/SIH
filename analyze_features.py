"""Measure features of all training data to find real separation boundaries."""
import sys, os, numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from ml_core import extract_features

FORMATS = ('.wav','.mp3','.ogg','.m4a','.flac','.webm','.aac')

def analyze(folder, label):
    pitches, rmss, specs = [], [], []
    files = [f for f in sorted(os.listdir(folder)) if f.lower().endswith(FORMATS)]
    for fname in files:
        try:
            feats, names = extract_features(os.path.join(folder, fname))
            fd = dict(zip(names, feats.tolist()))
            pitches.append(fd.get('pitch_std', 0))
            rmss.append(fd.get('rms_std', 0))
            specs.append(fd.get('spec_flatness_mean', 0))
        except: pass
    if not pitches:
        print(f"  {label}: no files")
        return
    print(f"\n{label} ({len(pitches)} files):")
    print(f"  pitch_std   min={min(pitches):.2f}  max={max(pitches):.2f}  mean={np.mean(pitches):.2f}  median={np.median(pitches):.2f}")
    print(f"  rms_std     min={min(rmss):.5f}  max={max(rmss):.5f}  mean={np.mean(rmss):.5f}")
    print(f"  spec_flat   min={min(specs):.5f}  max={max(specs):.5f}  mean={np.mean(specs):.5f}")
    # Show individual pitch values sorted
    sorted_p = sorted(pitches)
    print(f"  pitch sorted: {[round(x,1) for x in sorted_p]}")
    return pitches, rmss

print("="*60)
print("FEATURE DISTRIBUTION ANALYSIS")
print("="*60)

# ElevenLabs fakes only
el_files = [f for f in os.listdir('dataset/fake') if 'el_' in f and f.endswith('.mp3')]
el_pitches, el_rms = [], []
for fname in sorted(el_files):
    try:
        feats, names = extract_features(os.path.join('dataset/fake', fname))
        fd = dict(zip(names, feats.tolist()))
        el_pitches.append(fd.get('pitch_std', 0))
        el_rms.append(fd.get('rms_std', 0))
    except: pass

print(f"\nElevenLabs fakes only ({len(el_pitches)} files):")
if el_pitches:
    print(f"  pitch_std: min={min(el_pitches):.1f}  max={max(el_pitches):.1f}  mean={np.mean(el_pitches):.1f}")
    print(f"  rms_std:   min={min(el_rms):.5f}  max={max(el_rms):.5f}")
    print(f"  pitch sorted: {sorted([round(x,1) for x in el_pitches])}")

# User's real voice
print("\nUser's REAL voice:")
try:
    feats, names = extract_features('uploads/mic_1788616808_recording.webm')
    fd = dict(zip(names, feats.tolist()))
    print(f"  pitch_std  : {fd.get('pitch_std',0):.2f} Hz")
    print(f"  rms_std    : {fd.get('rms_std',0):.5f}")
    print(f"  spec_flat  : {fd.get('spec_flatness_mean',0):.5f}")
    user_pitch = fd.get('pitch_std', 0)
    user_rms   = fd.get('rms_std', 0)
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "="*60)
if el_pitches:
    max_el_pitch = max(el_pitches)
    print(f"Max ElevenLabs pitch_std : {max_el_pitch:.1f} Hz")
    print(f"User real pitch_std      : {user_pitch:.1f} Hz")
    gap = user_pitch - max_el_pitch
    print(f"Separation gap           : {gap:.1f} Hz")
    if gap > 3:
        print("Good separation - can set threshold safely")
        safe_thresh = max_el_pitch + gap * 0.4
        print(f"Recommended threshold    : {safe_thresh:.1f} Hz (pitch_std >= this = REAL)")
    else:
        print("POOR separation - need different features")
print("="*60)
