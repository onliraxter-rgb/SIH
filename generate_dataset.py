"""
VoiceGuard — ElevenLabs Dataset Generator
==========================================
Generates Hindi fake voice audio files for training dataset.

Usage:
  1. Set your API key below (ELEVENLABS_API_KEY)
  2. Run: python generate_dataset.py

Output: dataset/fake/ folder with MP3 files
"""

import os
import time
import requests

# ── SET YOUR API KEY HERE ──────────────────────────────────────────────────────
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_API_KEY_HERE")
# ──────────────────────────────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "dataset", "fake")

# ElevenLabs voices — use variety for better generalization
VOICES = [
    ("21m00Tcm4TlvDq8ikWAM", "Rachel"),
    ("AZnzlk1XvdvUeBnXmlld", "Domi"),
    ("EXAVITQu4vr4xnSDxMaL", "Bella"),
]

# Hindi sentences — varied topics for diverse training data
HINDI_TEXTS = [
    # Scam scenarios
    "नमस्ते, मैं आपके बैंक से बोल रहा हूं। आपका खाता बंद होने वाला है।",
    "आपके बेटे का एक्सीडेंट हो गया है। तुरंत पैसे भेजें।",
    "मैं RBI अधिकारी बोल रहा हूं, आपका खाता संदिग्ध है।",
    "बधाई हो, आप लकी ड्रॉ में पचास लाख रुपए जीत गए हैं।",
    "आपकी SIM बंद होने वाली है, KYC अपडेट करें।",
    "मुझे आपसे एक जरूरी बात करनी है, कृपया ध्यान दें।",
    "Namaste, main aapka bank adhikari bol raha hoon.",
    "Bhai mujhe urgent paisa chahiye, please abhi bhejo.",
    "Aapka account suspicious activity ke karan band ho sakta hai.",
    "RBI ki taraf se bol raha hoon, turant response karein.",
    # Neutral / everyday (so model learns AI patterns, not just scam words)
    "आज मौसम बहुत अच्छा है, बाहर घूमने का मन है।",
    "मेरा नाम राहुल है और मैं दिल्ली में रहता हूं।",
    "कल हम सब मिलकर खाना खाने गए थे।",
    "बाजार में आज नई सब्जियां आई हैं।",
    "मुझे किताबें पढ़ना बहुत पसंद है।",
    "The weather is very nice today.",
    "Please call me back when you get a chance.",
    "I am calling to inform you about an important update.",
    "Your package has been delivered to the front door.",
    "Thank you for your patience and cooperation.",
]


def generate(text: str, voice_id: str, output_path: str) -> bool:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.2,
            "use_speaker_boost": True,
        },
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(r.content)
            return True
        else:
            print(f"       API error {r.status_code}: {r.text[:80]}")
            return False
    except Exception as e:
        print(f"       Request failed: {e}")
        return False


def main():
    if ELEVENLABS_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please set your ElevenLabs API key in generate_dataset.py")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("═" * 52)
    print("  VoiceGuard — ElevenLabs Dataset Generator")
    print("═" * 52)
    print(f"\n  Output → {OUTPUT_DIR}")
    print(f"  Texts  : {len(HINDI_TEXTS)}")
    print(f"  Voices : {len(VOICES[:2])} (using first 2 to save credits)")
    print(f"  Total  : {len(HINDI_TEXTS) * 2} files\n")

    count = 0
    skipped = 0
    failed = 0

    for i, text in enumerate(HINDI_TEXTS):
        for j, (voice_id, voice_name) in enumerate(VOICES[:2]):
            filename = f"fake_{i + 1:03d}_v{j + 1}_{voice_name.lower()}.mp3"
            out_path = os.path.join(OUTPUT_DIR, filename)

            if os.path.exists(out_path):
                print(f"  ⏭  Skipping (exists): {filename}")
                skipped += 1
                continue

            short_text = (text[:45] + "…") if len(text) > 45 else text
            print(f"  ⏳  [{i+1}/{len(HINDI_TEXTS)}] {filename}")
            print(f"       Voice: {voice_name} | Text: {short_text}")

            if generate(text, voice_id, out_path):
                print(f"       ✅ Saved")
                count += 1
            else:
                failed += 1

            time.sleep(0.8)   # gentle rate limiting

    print(f"\n  ─────────────────────────────")
    print(f"  Generated : {count}")
    print(f"  Skipped   : {skipped}")
    print(f"  Failed    : {failed}")
    print(f"\n  Next steps:")
    print(f"  1. Record 20-30 real Hindi voice clips → dataset/real/")
    print(f"  2. Run: python train.py")
    print("═" * 52 + "\n")


if __name__ == "__main__":
    main()
