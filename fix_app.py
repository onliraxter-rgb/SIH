import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace file upload
code = code.replace(
    'filename, filepath = _save_upload(file)\n    result = detector.predict(filepath)\n\n    log_scan(',
    'filename, filepath = _save_upload(file)\n    result = detector.predict(filepath, source="file_upload")\n\n    log_scan('
)

# Replace mic upload
code = code.replace(
    'filename, filepath = _save_upload(file, prefix="mic")\n    result = detector.predict(filepath)\n\n    log_scan(',
    'filename, filepath = _save_upload(file, prefix="mic")\n    result = detector.predict(filepath, source="live_mic")\n\n    log_scan('
)

# Replace simulator
code = code.replace(
    '# Analyze\n    result = detector.predict(filepath)\n\n    log_scan(',
    '# Analyze\n    result = detector.predict(filepath, source="scam_simulator")\n\n    log_scan('
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated app.py successfully.")
