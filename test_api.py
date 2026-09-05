import sys, requests
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = 'http://127.0.0.1:5000'

print("Test 1 - Your real voice recording:")
with open('uploads/mic_1788616808_recording.webm', 'rb') as f:
    r = requests.post(BASE + '/api/scan-mic',
        files={'audio': ('recording.webm', f, 'audio/webm')}, timeout=30)
d = r.json()
status = d.get("status")
conf   = d.get("confidence")
pitch  = d.get("features", {}).get("pitch_variance_hz")
rms    = d.get("features", {}).get("voice_dynamics")
mused  = d.get("model_used")
reason = d.get("verdict_reason", "")[:80]
print("  Status    :", status)
print("  Confidence:", conf, "%")
print("  Pitch Hz  :", pitch)
print("  RMS       :", rms)
print("  Model     :", mused)
print("  Reason    :", reason)

print()
print("Test 2 - ElevenLabs generated FAKE:")
with open('uploads/sim_1788614070.mp3', 'rb') as f:
    r = requests.post(BASE + '/api/scan-file',
        files={'audio': ('fake.mp3', f, 'audio/mpeg')}, timeout=30)
d = r.json()
status2 = d.get("status")
conf2   = d.get("confidence")
pitch2  = d.get("features", {}).get("pitch_variance_hz")
mused2  = d.get("model_used")
print("  Status    :", status2)
print("  Confidence:", conf2, "%")
print("  Pitch Hz  :", pitch2)
print("  Model     :", mused2)

print()
if status == "REAL" and status2 == "FAKE":
    print("PERFECT - Real=REAL, Fake=FAKE. Working correctly!")
elif status == "REAL":
    print("PARTIAL - Real voice fixed. Fake detection:", status2)
else:
    print("STILL WRONG - Real voice still classified as:", status)
