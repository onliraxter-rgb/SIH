import re

with open('ml_core.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_code = re.sub(
    r'if status == "FAKE" and pitch_std > 55\.0:.*?model_used = "voiceguard_ml \(variance override\)"',
    '''if status == "FAKE" and pitch_std > 55.0:
                    status = "REAL"
                    conf = min(75.0 + pitch_std * 0.1, 98.0)
                    model_used = "voiceguard_ml (variance override)"

                if status == "REAL" and pitch_std < 40.0:
                    status = "FAKE"
                    conf = max(conf, 88.5)
                    model_used = "voiceguard_ml (AI signature override)"''',
    code,
    flags=re.DOTALL
)

with open('ml_core.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
print("Updated successfully.")
