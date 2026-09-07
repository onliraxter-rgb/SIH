import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('make_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace CSS variables block with beige + dark black theme
old_vars = """:root {
  --bg: #0f172a;
  --surface: #1e293b;
  --surface2: #263348;
  --border: #334155;
  --border-light: #3d4f69;
  --text: #f1f5f9;
  --text2: #cbd5e1;
  --muted: #64748b;
  --green: #10b981;
  --green-dim: #064e3b;
  --red: #ef4444;
  --red-dim: #450a0a;
  --blue: #3b82f6;
  --blue-dim: #1e3a5f;
  --amber: #f59e0b;
}"""

new_vars = """:root {
  --bg: #0c0c0c;
  --surface: #141414;
  --surface2: #1c1c1c;
  --border: #2a2a2a;
  --border-light: #3a3a3a;
  --text: #e8dcc8;
  --text2: #c9b99a;
  --muted: #7a6e5c;
  --green: #c8a96e;
  --green-dim: #2a200e;
  --red: #e05c4b;
  --red-dim: #2a0e0a;
  --blue: #c8a96e;
  --blue-dim: #2a200e;
  --amber: #d4904a;
}"""

code = code.replace(old_vars, new_vars)

# Fix logo icon color to use warm amber
code = code.replace(
    '.logo-icon { width: 32px; height: 32px; background: var(--blue); border-radius: 8px;',
    '.logo-icon { width: 32px; height: 32px; background: #c8a96e; border-radius: 8px;'
)

# Fix logo text accent
code = code.replace(
    '.logo-text span { color: var(--blue); }',
    '.logo-text span { color: #c8a96e; }'
)

# Fix step num color
code = code.replace(
    '.step-num { width: 24px; height: 24px; border-radius: 50%; border: 1px solid var(--border-light); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: var(--blue); flex-shrink: 0; }',
    '.step-num { width: 24px; height: 24px; border-radius: 50%; border: 1px solid #3a3a3a; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #c8a96e; flex-shrink: 0; }'
)

# Fix scrollbar
code = code.replace(
    '::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }',
    '::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }'
)

# Fix waveform idle color
code = code.replace(
    "ctx.strokeStyle = '#334155';",
    "ctx.strokeStyle = '#3a3a3a';"
)

# Fix loading bar color
code = code.replace(
    '.loading-bar-fill { height: 100%; background: var(--blue);',
    '.loading-bar-fill { height: 100%; background: #c8a96e;'
)

# Fix loading spinner
code = code.replace(
    '.loading-spinner { width: 18px; height: 18px; border: 2px solid var(--border); border-top-color: var(--blue);',
    '.loading-spinner { width: 18px; height: 18px; border: 2px solid #2a2a2a; border-top-color: #c8a96e;'
)

# Fix mic btn hover border to beige
code = code.replace(
    '.mic-btn:hover { background: #2d3f5a; border-color: var(--blue); transform: scale(1.02); }',
    '.mic-btn:hover { background: #242424; border-color: #c8a96e; transform: scale(1.02); }'
)

# Fix tab active color
code = code.replace(
    '.mic-tab.active { background: var(--surface2); color: var(--text); border: 1px solid var(--border); }',
    '.mic-tab.active { background: #1c1c1c; color: #e8dcc8; border: 1px solid #3a3a3a; }'
)

# Fix conf bar green and red  
code = code.replace(
    ".bar-fill.green { background: linear-gradient(90deg, #059669, #10b981); }",
    ".bar-fill.green { background: linear-gradient(90deg, #a07830, #c8a96e); }"
)

# Fix radar grid colors
code = code.replace(
    "grid:{color:'rgba(51,65,85,0.8)'}",
    "grid:{color:'rgba(42,42,42,0.9)'}"
)
code = code.replace(
    "angleLines:{color:'rgba(51,65,85,0.8)'}",
    "angleLines:{color:'rgba(42,42,42,0.9)'}"
)

# Fix voice card selected color
code = code.replace(
    ".voice-card.sel { border-color: var(--blue); background: rgba(59,130,246,0.08); color: var(--blue); }",
    ".voice-card.sel { border-color: #c8a96e; background: rgba(200,169,110,0.08); color: #c8a96e; }"
)

# Fix textarea focus
code = code.replace(
    "textarea.sim-input:focus { border-color: var(--blue); }",
    "textarea.sim-input:focus { border-color: #c8a96e; }"
)

# Fix dropzone hover
code = code.replace(
    ".dropzone:hover, .dropzone.over { border-color: var(--blue); background: rgba(59,130,246,0.04); }",
    ".dropzone:hover, .dropzone.over { border-color: #c8a96e; background: rgba(200,169,110,0.04); }"
)

# Fix btn-primary background
code = code.replace(
    ".btn-primary { background: var(--blue); color: #fff; }",
    ".btn-primary { background: #c8a96e; color: #0c0c0c; }"
)
code = code.replace(
    ".btn-primary:hover { background: #2563eb; transform: translateY(-1px); }",
    ".btn-primary:hover { background: #b8935a; transform: translateY(-1px); }"
)

# Fix stat-box val colors in HTML
code = code.replace(
    'style="color:var(--blue)">—',
    'style="color:#c8a96e">—'
)
code = code.replace(
    'style="color:var(--blue)">0',
    'style="color:#c8a96e">0'
)

# body background color
code = code.replace(
    'body { background: var(--bg); color: var(--text); font-family: \'Inter\', sans-serif; min-height: 100vh; font-size: 14px; line-height: 1.5; }',
    'body { background: var(--bg); color: var(--text); font-family: \'Inter\', sans-serif; min-height: 100vh; font-size: 14px; line-height: 1.5; letter-spacing: 0.01em; }'
)

with open('make_html.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Theme updated to Beige + Black.")
