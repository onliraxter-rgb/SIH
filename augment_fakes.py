import os
import glob
import librosa
import soundfile as sf
import numpy as np

def simulate_mic_recording(y, sr):
    # 1. Bandpass filter to simulate phone speaker (300Hz - 3400Hz)
    y_filt = librosa.effects.preemphasis(y, coef=0.85)
    
    # 2. Add room/mic background noise (white noise)
    noise_amp = 0.005 * np.random.uniform(0.5, 1.5)
    noise = noise_amp * np.random.normal(size=y.shape)
    y_noisy = y_filt + noise
    
    # 3. Simulate mic distance (slight reverb/echo)
    # Simple delay line
    delay_samples = int(sr * 0.02) # 20ms delay
    decay = 0.3
    y_reverb = np.zeros_like(y_noisy)
    y_reverb[:] = y_noisy
    y_reverb[delay_samples:] += y_noisy[:-delay_samples] * decay
    
    # Normalize to prevent clipping
    if np.max(np.abs(y_reverb)) > 0:
        y_reverb = y_reverb / np.max(np.abs(y_reverb)) * 0.9
        
    return y_reverb

fake_files = glob.glob('dataset/fake/*.*')
print(f"Found {len(fake_files)} fake files to augment.")

os.makedirs('dataset/fake', exist_ok=True)

count = 0
for f in fake_files:
    if 'mic_sim_' in f: continue
    try:
        y, sr = librosa.load(f, sr=16000)
        y_sim = simulate_mic_recording(y, sr)
        
        out_name = os.path.join('dataset/fake', 'mic_sim_' + os.path.basename(f).split('.')[0] + '.wav')
        sf.write(out_name, y_sim, sr)
        count += 1
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Successfully created {count} mic-simulated fake voices!")
