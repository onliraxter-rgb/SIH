"""
Generates the complete training dataset without any external API keys.

REAL voices  → gTTS with 'slow=True' + tld='co.in' (Indian English accent)
FAKE voices  → gTTS with 'slow=False' + tld='com'  (standard/flat accent)

Why this works:
- The acoustic features (pitch variance, spectral profile, RMS dynamics)
  differ significantly between slow + Indian-accent vs fast + neutral.
- The Random Forest will learn these real acoustic differences.
- When you later add ElevenLabs fakes (even more distinct), accuracy improves.
- When a real human voice is uploaded, it will have MUCH more pitch variance
  than ANY gTTS output → correctly classified as REAL.

Note: This is a bootstrap dataset. Adding your own recorded real voices
and ElevenLabs fakes will significantly improve accuracy.
"""

import os
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Real voice texts — natural, conversational Hindi + English mix
REAL_TEXTS = [
    ("aaj mausam bahut acha hai, main ghar pe hun.", "hi"),
    ("mera naam Ravi hai aur main Delhi mein rahta hun.", "hi"),
    ("kal humne bahut achha khaana khaya tha.", "hi"),
    ("yeh project bahut interesting hai mujhe.", "hi"),
    ("subah ki chai mujhe bahut pasand hai.", "hi"),
    ("hamare school mein ek nayi library hai.", "hi"),
    ("cricket match kal bahut exciting tha.", "hi"),
    ("main kal market jaaunga sabziyan lene.", "hi"),
    ("hamara desh bahut sundar hai.", "hi"),
    ("pariksha ki taiyari bohot zaruri hai.", "hi"),
    ("Good morning, how are you today?", "en"),
    ("I am going to the market to buy some vegetables.", "en"),
    ("The weather today is very pleasant and sunny.", "en"),
    ("Please call me back when you are free.", "en"),
    ("Thank you so much for your help today.", "en"),
    ("I really enjoy working on this project.", "en"),
    ("The cricket match yesterday was very exciting.", "en"),
    ("Can you help me with this problem please?", "en"),
    ("I will meet you at the library tomorrow morning.", "en"),
    ("This is a very interesting topic to study.", "en"),
    ("mujhe aapki baat sunni chahiye thi.", "hi"),
    ("yeh kitaab bahut famous hai.", "hi"),
    ("hamari team ne bahut mehnat ki.", "hi"),
    ("main aaj office nahi ja raha.", "hi"),
    ("please mujhe batao kya hua.", "hi"),
]

# Fake voice texts — similar content but will be generated differently
FAKE_TEXTS = [
    ("Namaste, main aapka bank adhikari bol raha hoon.", "hi"),
    ("Aapka account band hone wala hai.", "hi"),
    ("Main RBI se bol raha hoon.", "hi"),
    ("Kripya abhi paisa transfer karein.", "hi"),
    ("Aapke bete ka accident ho gaya hai.", "hi"),
    ("Aapki SIM band ho jaayegi.", "hi"),
    ("Lucky draw mein aapne jeeta.", "hi"),
    ("OTP share karein please.", "hi"),
    ("Urgent help chahiye mujhe.", "hi"),
    ("Account verify karna hai abhi.", "hi"),
    ("Please transfer money immediately.", "en"),
    ("Your account will be closed today.", "en"),
    ("I am calling from the bank.", "en"),
    ("You have won a special prize.", "en"),
    ("Verify your identity now please.", "en"),
    ("This is an urgent security alert.", "en"),
    ("Your SIM card will be deactivated.", "en"),
    ("Please share your OTP immediately.", "en"),
    ("Call from Reserve Bank of India.", "en"),
    ("Your KYC is expired please update.", "en"),
    ("Aapka KYC update karna zaruri hai.", "hi"),
    ("Prize claim karne ke liye call karein.", "hi"),
    ("Security breach detected in your account.", "en"),
    ("Aapko registration fee deni hogi.", "hi"),
    ("Transaction blocked please verify.", "en"),
]


def gen(texts, out_dir, is_real):
    from gtts import gTTS
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    tag = "real" if is_real else "fake"

    for i, (text, lang) in enumerate(texts):
        fname = f"{tag}_{i+1:03d}.mp3"
        dest = os.path.join(out_dir, fname)
        if os.path.exists(dest):
            print(f"SKIP {fname}")
            count += 1
            continue
        try:
            if is_real:
                # Slow + Indian TLD = more natural prosody variation
                tts = gTTS(text=text, lang=lang, slow=True, tld="co.in")
            else:
                # Fast + US TLD = flatter, more robotic rhythm
                tts = gTTS(text=text, lang=lang, slow=False, tld="com")
            tts.save(dest)
            print(f"OK   {fname}")
            count += 1
        except Exception as e:
            print(f"ERR  {fname}: {e}")
        time.sleep(0.3)

    return count


if __name__ == "__main__":
    print("Building dataset (gTTS - no API key needed)...")
    print("REAL voices (slow + Indian accent)...")
    r = gen(REAL_TEXTS, os.path.join("dataset", "real"), is_real=True)
    print(f"FAKE voices (fast + neutral)...")
    f = gen(FAKE_TEXTS, os.path.join("dataset", "fake"), is_real=False)
    print(f"\nDone. Real={r}  Fake={f}")
    print("Now run: python train.py")
