import sys, requests
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
API_KEY = 'sk_e965d7392f9bed5d878fd846f79404a16d8c86270c8503a3'
headers = {'xi-api-key': API_KEY, 'Content-Type': 'application/json'}

# Get all voices available on this account
r = requests.get('https://api.elevenlabs.io/v1/voices', headers={'xi-api-key': API_KEY})
voices = r.json().get('voices', [])
print(f'Available voices: {len(voices)}')
for v in voices:
    print(f'  {v["voice_id"]}  {v["name"]}  category={v.get("category")}')

# Try each voice with eleven_flash_v2 (usually free-tier accessible)
for v in voices[:5]:
    vid = v['voice_id']
    r2 = requests.post(
        f'https://api.elevenlabs.io/v1/text-to-speech/{vid}',
        json={'text': 'Hello, this is a test voice.', 'model_id': 'eleven_flash_v2'},
        headers=headers, timeout=15
    )
    print(f'  Voice {v["name"]} ({vid}): HTTP {r2.status_code}')
    if r2.status_code == 200:
        print('  -> WORKS! Saving...')
        open('test_voice.mp3', 'wb').write(r2.content)
        break
    else:
        print(f'  -> {r2.text[:100]}')
