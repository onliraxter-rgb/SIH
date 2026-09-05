import sys, os, time, requests
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_KEY = 'sk_e965d7392f9bed5d878fd846f79404a16d8c86270c8503a3'
OUT_DIR = os.path.join('dataset', 'fake')
os.makedirs(OUT_DIR, exist_ok=True)

# Working voices from free plan (confirmed HTTP 200)
VOICES = [
    ('CwhRBWXzGAHq8TQ4Fs17', 'Roger'),
    ('EXAVITQu4vr4xnSDxMaL', 'Sarah'),
    ('JBFqnCBsd6RMkjVDRZzb', 'George'),
    ('nPczCjzI2devNBz1zQrb', 'Brian'),
    ('onwK4e9ZLuTAKqWW03F9', 'Daniel'),
]

TEXTS = [
    'Namaste, main aapka bank adhikari bol raha hoon. Aapka account band hone wala hai.',
    'Main RBI se bol raha hoon. Aapke account mein suspicious activity detect hui hai.',
    'Bhai, mujhe bahut bura accident hua hai. Please urgent paisa bhejo.',
    'Aapki SIM card aaj raat band ho jaayegi. Abhi verify karein.',
    'Badhai ho! Aap lucky draw mein 50 lakh rupaye jeet gaye hain.',
    'Kripya apna OTP abhi share karein warna account block ho jaayega.',
    'Main aapke bank ki security team se bol raha hoon.',
    'Aapka KYC expire ho gaya hai, turant update karein.',
    'This is an urgent message from your bank. Please verify immediately.',
    'Your account has been flagged for suspicious activity. Call us now.',
    'Congratulations, you have won a special prize. Claim it today.',
    'Please transfer the amount immediately to avoid account suspension.',
    'I am calling from Reserve Bank of India regarding your account.',
    'Your SIM will be deactivated in 2 hours. Please verify your KYC.',
    'Security alert: unauthorized login detected on your account.',
    'Please share your card details to complete the verification process.',
    'Your electricity connection will be cut in one hour. Pay now.',
    'This is a recorded message from your bank. Action required immediately.',
    'We have detected fraud on your account. Please confirm your details.',
    'You are selected for a government scheme. Claim your benefit now.',
]

headers = {'xi-api-key': API_KEY, 'Content-Type': 'application/json'}
count = 0

for i, text in enumerate(TEXTS):
    voice_id, voice_name = VOICES[i % len(VOICES)]
    fname = f'fake_el_{i+1:03d}_{voice_name.lower()}.mp3'
    dest  = os.path.join(OUT_DIR, fname)
    if os.path.exists(dest):
        print(f'SKIP {fname}')
        count += 1
        continue
    payload = {
        'text': text,
        'model_id': 'eleven_multilingual_v2',
        'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}
    }
    try:
        r = requests.post(
            f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
            json=payload, headers=headers, timeout=30
        )
        if r.status_code == 200:
            open(dest, 'wb').write(r.content)
            print(f'OK   {fname}  ({len(r.content)} bytes)')
            count += 1
        elif r.status_code == 402:
            # Try flash model instead
            payload['model_id'] = 'eleven_flash_v2_5'
            r2 = requests.post(
                f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
                json=payload, headers=headers, timeout=30
            )
            if r2.status_code == 200:
                open(dest, 'wb').write(r2.content)
                print(f'OK   {fname} (flash model)  ({len(r2.content)} bytes)')
                count += 1
            else:
                print(f'ERR  {fname}: {r2.status_code} {r2.text[:60]}')
        else:
            print(f'ERR  {fname}: HTTP {r.status_code} {r.text[:60]}')
    except Exception as e:
        print(f'FAIL {fname}: {e}')
    time.sleep(0.5)

print(f'\nDone: {count}/{len(TEXTS)} ElevenLabs fakes generated')
