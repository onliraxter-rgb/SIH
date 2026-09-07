from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Colour Palette (matches the site) ──
BLACK   = RGBColor(0x00, 0x00, 0x00)
BG1     = RGBColor(0x08, 0x08, 0x08)
CARD    = RGBColor(0x12, 0x12, 0x12)
BORDER  = RGBColor(0x26, 0x26, 0x26)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
GREY    = RGBColor(0x99, 0x99, 0x99)
LGREY   = RGBColor(0xE5, 0xE5, 0xE5)
RED     = RGBColor(0xD9, 0x5F, 0x4B)
GREEN   = RGBColor(0x6A, 0xAB, 0x7E)
DGREEN  = RGBColor(0x1C, 0x2E, 0x22)
DRED    = RGBColor(0x2E, 0x10, 0x10)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # completely blank

# ── helper: add a solid rectangle ──────────────────────────────────────────
def rect(slide, l, t, w, h, fill_rgb, border_rgb=None, border_pt=0):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    shape.line.width = Pt(border_pt)
    if border_rgb:
        shape.line.color.rgb = border_rgb
    else:
        shape.line.fill.background()
    return shape

# ── helper: add text box ───────────────────────────────────────────────────
def txt(slide, text, l, t, w, h,
        size=18, bold=False, italic=False, color=WHITE,
        align=PP_ALIGN.LEFT, wrap=True, font="Inter"):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb

# ── helper: multi-line text box ────────────────────────────────────────────
def mtxt(slide, lines, l, t, w, h,
         size=14, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
         line_color=None, font="Inter"):
    from pptx.util import Pt
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = line_color if line_color else color
    return txb

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 1 — TITLE
# ─────────────────────────────────────────────────────────────────────────────
s1 = prs.slides.add_slide(BLANK)
rect(s1, 0,0, 13.33,7.5, BLACK)                          # bg
rect(s1, 0,0, 13.33,0.06, WHITE)                          # top stripe
rect(s1, 0,7.44,13.33,0.06, WHITE)                        # bottom stripe

# Left accent bar
rect(s1, 0.55, 2.1, 0.06, 3.3, WHITE)

# Tagline chip
rect(s1, 0.75, 2.1, 2.5, 0.38, CARD, BORDER, 0.5)
txt(s1, "SIH 2026  ·  SIH26104", 0.82, 2.14, 2.4, 0.3,
    size=10, color=GREY, align=PP_ALIGN.LEFT)

# Title
txt(s1, "VoiceGuard AI", 0.75, 2.65, 8, 1.2,
    size=64, bold=True, color=WHITE, font="Calibri")

# Subtitle
txt(s1, "Real-Time AI Voice Clone Detection System",
    0.75, 3.9, 10, 0.55, size=22, color=LGREY)

# Description
txt(s1, "Detect AI-cloned voices instantly — protecting people from deepfake scams, fraud calls, and voice impersonation.",
    0.75, 4.55, 9, 0.7, size=14, color=GREY)

# Right visual — fake mic circle
rect(s1, 9.8, 1.9, 2.8, 2.8, CARD, BORDER, 0.5)
txt(s1, "🎙", 10.8, 2.6, 1.0, 1.0, size=48, align=PP_ALIGN.CENTER)
txt(s1, "ANALYZING", 9.9, 3.6, 2.6, 0.4, size=10, color=GREY,
    align=PP_ALIGN.CENTER)

# Bottom
txt(s1, "Python  ·  Flask  ·  scikit-learn  ·  librosa  ·  ElevenLabs  ·  Cloudflare",
    0.75, 6.9, 12, 0.4, size=11, color=GREY)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 2 — PROBLEM STATEMENT
# ─────────────────────────────────────────────────────────────────────────────
s2 = prs.slides.add_slide(BLANK)
rect(s2, 0,0,13.33,7.5, BLACK)
rect(s2, 0,0,13.33,0.06, WHITE)
rect(s2, 0,7.44,13.33,0.06, WHITE)

txt(s2, "The Problem", 0.6, 0.25, 6, 0.55, size=11, color=GREY)
txt(s2, "AI Voice Cloning is a\nGrowing Threat", 0.6, 0.7, 8, 1.4,
    size=34, bold=True, color=WHITE, font="Calibri")

txt(s2, "Modern AI tools like ElevenLabs can clone any person's voice from just 30 seconds of audio — and it's free.",
    0.6, 2.2, 8.5, 0.6, size=15, color=LGREY)

threats = [
    ("📞", "Phone Scams", "Fake child/relative voice: \"Mom, I'm in jail, send ₹50,000 now\""),
    ("🏦", "Bank Fraud",   "Cloned CEO voice authorizing fake wire transfers over phone"),
    ("🎙️", "Deepfakes",    "Fake politicians, celebrities spreading misinformation via voice"),
    ("👮", "ID Theft",     "Bypassing bank voice authentication with a cloned voice"),
]

for i, (icon, title, desc) in enumerate(threats):
    col = i % 2
    row = i // 2
    lf = 0.6 + col * 6.5
    tp = 3.0 + row * 1.7
    rect(s2, lf, tp, 6.1, 1.45, CARD, BORDER, 0.5)
    txt(s2, icon, lf+0.15, tp+0.25, 0.6, 0.8, size=26)
    txt(s2, title, lf+0.85, tp+0.2, 5.0, 0.38, size=14, bold=True, color=WHITE)
    txt(s2, desc,  lf+0.85, tp+0.62, 5.0, 0.65, size=11, color=GREY)

rect(s2, 0.6, 6.75, 12.1, 0.55, DRED, RED, 0.5)
txt(s2, "⚠  In 2024, AI voice scams caused over $25 billion in global losses. Detection tools are critically lacking.",
    0.8, 6.8, 12, 0.4, size=11, color=RED)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 3 — SOLUTION OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
s3 = prs.slides.add_slide(BLANK)
rect(s3, 0,0,13.33,7.5, BLACK)
rect(s3, 0,0,13.33,0.06, WHITE)
rect(s3, 0,7.44,13.33,0.06, WHITE)

txt(s3, "Our Solution", 0.6, 0.25, 6, 0.4, size=11, color=GREY)
txt(s3, "VoiceGuard AI", 0.6, 0.65, 8, 0.8, size=40, bold=True, color=WHITE, font="Calibri")
txt(s3, "Three ways to detect AI clones instantly", 0.6, 1.5, 9, 0.4, size=16, color=GREY)

features = [
    ("🎤", "Live Microphone", "Speak into the mic for 5 seconds. Get an instant REAL or FAKE verdict with acoustic breakdown.", GREEN),
    ("📁", "File Upload",     "Upload any .mp3, .wav, .ogg, .m4a file. Analyze recordings, voice notes, call recordings.", WHITE),
    ("🤖", "Scam Simulator",  "Type a scam message → ElevenLabs generates a real AI clone → VoiceGuard catches it live.", RED),
]

for i, (icon, title, desc, col) in enumerate(features):
    lf = 0.5 + i * 4.25
    rect(s3, lf, 2.15, 3.95, 3.5, CARD, BORDER, 0.5)
    txt(s3, icon, lf+0.2, 2.35, 0.8, 0.8, size=32)
    txt(s3, title, lf+0.2, 3.15, 3.5, 0.45, size=15, bold=True, color=col)
    txt(s3, desc,  lf+0.2, 3.65, 3.6, 1.6, size=12, color=GREY)

txt(s3, "All three modes run the same ML pipeline — real-time acoustic feature extraction + Logistic Regression classifier",
    0.6, 5.9, 12.1, 0.45, size=12, color=GREY, align=PP_ALIGN.CENTER)

rect(s3, 0.6, 6.45, 12.1, 0.75, CARD, BORDER, 0.5)
stats = [
    ("51", "Training Samples"),
    ("66", "Acoustic Features"),
    ("98%", "Cross-Val Accuracy"),
    ("<2s", "Detection Time"),
]
for i, (val, lbl) in enumerate(stats):
    lf = 1.4 + i*3.0
    txt(s3, val, lf, 6.48, 2.5, 0.4, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER, font="Calibri")
    txt(s3, lbl, lf, 6.88, 2.5, 0.25, size=10, color=GREY, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 4 — HOW IT WORKS (TECHNICAL)
# ─────────────────────────────────────────────────────────────────────────────
s4 = prs.slides.add_slide(BLANK)
rect(s4, 0,0,13.33,7.5, BLACK)
rect(s4, 0,0,13.33,0.06, WHITE)
rect(s4, 0,7.44,13.33,0.06, WHITE)

txt(s4, "Technical Architecture", 0.6, 0.25, 6, 0.4, size=11, color=GREY)
txt(s4, "How It Works", 0.6, 0.65, 8, 0.65, size=38, bold=True, color=WHITE, font="Calibri")

steps = [
    ("01", "Audio Capture", "WebM from mic / MP3-WAV file / ElevenLabs API synthesis", "16kHz mono, max 10s"),
    ("02", "Feature Extraction", "librosa extracts 66 acoustic features per file", "MFCC×40, pitch, RMS, ZCR, spectral flatness, chroma"),
    ("03", "ML Classification", "Logistic Regression (scikit-learn + StandardScaler pipeline)", "Trained on 11 real + 40 ElevenLabs fake samples"),
    ("04", "Verdict + Evidence", "REAL / FAKE + confidence % + acoustic radar chart", "Pitch variance, voice dynamics, spectral fingerprint"),
]

for i, (num, title, desc, detail) in enumerate(steps):
    lf = 0.5 + i * 3.2
    rect(s4, lf, 1.6, 3.0, 4.2, CARD, BORDER, 0.5)
    txt(s4, num,    lf+0.2, 1.75, 2.8, 0.55, size=28, bold=True, color=BORDER, font="Calibri")
    txt(s4, title,  lf+0.2, 2.3,  2.7, 0.45, size=14, bold=True, color=WHITE)
    txt(s4, desc,   lf+0.2, 2.85, 2.7, 0.8,  size=11, color=LGREY)
    rect(s4, lf+0.2, 3.75, 2.65, 0.02, BORDER)
    txt(s4, detail, lf+0.2, 3.85, 2.7, 1.0,  size=10, color=GREY)
    # Arrow
    if i < 3:
        txt(s4, "→", lf+3.05, 3.4, 0.3, 0.4, size=18, color=BORDER, align=PP_ALIGN.CENTER)

# Key insight box
rect(s4, 0.5, 6.0, 12.3, 1.2, DGREEN, GREEN, 0.5)
txt(s4, "🔑  Key Insight", 0.75, 6.08, 4, 0.38, size=12, bold=True, color=GREEN)
txt(s4, "ElevenLabs AI voices are acoustically too perfect — pitch variance of only 5–15 Hz vs 30–80 Hz for real humans. Low spectral flatness, robotic steady volume. The ML model exploits these physical differences.",
    0.75, 6.48, 12.0, 0.6, size=11, color=LGREY)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 5 — WHY OUR APPROACH WORKS
# ─────────────────────────────────────────────────────────────────────────────
s5 = prs.slides.add_slide(BLANK)
rect(s5, 0,0,13.33,7.5, BLACK)
rect(s5, 0,0,13.33,0.06, WHITE)
rect(s5, 0,7.44,13.33,0.06, WHITE)

txt(s5, "The Science", 0.6, 0.25, 6, 0.4, size=11, color=GREY)
txt(s5, "Why AI Voices Are Detectable", 0.6, 0.65, 11, 0.7, size=36, bold=True, color=WHITE, font="Calibri")

# Feature comparison table
headers = ["Acoustic Feature", "Real Human Voice", "AI Cloned Voice"]
col_w = [4.0, 3.8, 3.8]
col_x = [0.6, 4.7, 8.6]

rect(s5, 0.5, 1.6, 12.2, 0.5, BORDER)
for j, h in enumerate(headers):
    txt(s5, h, col_x[j]+0.1, 1.65, col_w[j]-0.15, 0.38,
        size=11, bold=True, color=WHITE)

rows = [
    ("Pitch Variance (std Hz)", "30 – 80 Hz  (natural emotion)", "5 – 15 Hz  (unnaturally flat)"),
    ("Volume Dynamics (RMS std)", "0.05 – 0.12  (breathing, stress)", "0.002 – 0.01  (robotic steady)"),
    ("Spectral Flatness", "Low (0.01–0.04) — tonal voice", "Medium–High — noise-like synthesis"),
    ("Zero Crossing Rate", "Variable (consonants, pauses)", "Consistently smooth waveform"),
    ("MFCC Pattern", "Irregular vocal tract shifts", "Smooth, AI-interpolated transitions"),
]

for i, row in enumerate(rows):
    bg = CARD if i % 2 == 0 else BLACK
    rect(s5, 0.5, 2.15+i*0.85, 12.2, 0.82, bg, BORDER, 0.3)
    for j, cell in enumerate(row):
        c = WHITE if j == 0 else (GREEN if j == 1 else RED)
        txt(s5, cell, col_x[j]+0.1, 2.2+i*0.85, col_w[j]-0.15, 0.65, size=11, color=c)

txt(s5, "Our model uses ALL these features simultaneously — making it robust against future AI voice improvements.",
    0.6, 6.6, 12.0, 0.55, size=12, color=GREY, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 6 — DEMO FLOW
# ─────────────────────────────────────────────────────────────────────────────
s6 = prs.slides.add_slide(BLANK)
rect(s6, 0,0,13.33,7.5, BLACK)
rect(s6, 0,0,13.33,0.06, WHITE)
rect(s6, 0,7.44,13.33,0.06, WHITE)

txt(s6, "Live Demo", 0.6, 0.25, 6, 0.4, size=11, color=GREY)
txt(s6, "See It In Action", 0.6, 0.65, 9, 0.65, size=38, bold=True, color=WHITE, font="Calibri")

demos = [
    ("🤖", "Scam Simulator", RED,
     ['1. Go to "Scam Simulator" tab',
      '2. Type: "Mom, I\'m stuck at police',
      '   station. Send ₹50,000 now."',
      '3. Hit Generate & Detect Clone',
      '4. ElevenLabs synthesizes real AI voice',
      '5. System flags it → FAKE 🚨 (94%)',
      '   in under 2 seconds']),
    ("🎤", "Live Mic", GREEN,
     ['1. Go to "Microphone" tab',
      '2. Click the mic button',
      '3. Speak naturally for 5–8 seconds',
      '   (any sentence is fine)',
      '4. Click Stop, then Analyze',
      '5. System detects → REAL ✅ (87%+)',
      '   Shows pitch & dynamics chart']),
    ("📁", "File Upload", WHITE,
     ['1. Go to "Upload Audio" tab',
      '2. Drag & drop any MP3/WAV/OGG',
      '   (YouTube-downloaded news clip)',
      '3. Click Analyze File',
      '4. Gets full acoustic breakdown:',
      '   pitch variance, MFCC radar chart',
      '5. Verdict in under 3 seconds']),
]

for i, (icon, title, col, steps_list) in enumerate(demos):
    lf = 0.5 + i * 4.25
    rect(s6, lf, 1.65, 3.95, 5.4, CARD, BORDER, 0.5)
    rect(s6, lf, 1.65, 3.95, 0.55, BORDER)
    txt(s6, icon+" "+title, lf+0.2, 1.7, 3.6, 0.42, size=14, bold=True, color=col)
    for j, step in enumerate(steps_list):
        txt(s6, step, lf+0.2, 2.35+j*0.45, 3.6, 0.4, size=11, color=LGREY if not step.startswith("5.") else WHITE)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 7 — TECH STACK + PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
s7 = prs.slides.add_slide(BLANK)
rect(s7, 0,0,13.33,7.5, BLACK)
rect(s7, 0,0,13.33,0.06, WHITE)
rect(s7, 0,7.44,13.33,0.06, WHITE)

txt(s7, "Technology", 0.6, 0.25, 6, 0.4, size=11, color=GREY)
txt(s7, "Stack & Performance", 0.6, 0.65, 9, 0.65, size=38, bold=True, color=WHITE, font="Calibri")

# Left: Tech stack
txt(s7, "TECH STACK", 0.6, 1.55, 5.5, 0.35, size=10, bold=True, color=GREY)
stack = [
    ("⚙️  Backend",      "Python 3.10 + Flask — REST API, file handling, session management"),
    ("🧠  ML / Audio",   "scikit-learn (Logistic Regression)  ·  librosa (audio analysis)"),
    ("🎤  Audio APIs",   "Web Audio API (live waveform)  ·  MediaRecorder (mic capture)"),
    ("🤖  AI Synthesis", "ElevenLabs REST API — generates AI voice clones for the simulator"),
    ("🗄️  Database",     "SQLite — scan history, confidence logs, stats tracking"),
    ("☁️  Hosting",      "Cloudflare Zero Trust Tunnel — live public URL, no port forwarding"),
    ("🌐  Frontend",     "Vanilla JS + Chart.js — no frameworks, pure fast performance"),
]
for i, (label, desc) in enumerate(stack):
    rect(s7, 0.6, 2.0+i*0.66, 6.3, 0.6, CARD, BORDER, 0.3)
    txt(s7, label, 0.75, 2.05+i*0.66, 1.7, 0.42, size=10, bold=True, color=WHITE)
    txt(s7, desc,  2.45, 2.05+i*0.66, 4.3, 0.42, size=10, color=GREY)

# Right: Performance metrics
txt(s7, "PERFORMANCE", 7.3, 1.55, 5.5, 0.35, size=10, bold=True, color=GREY)
metrics = [
    ("100%",  "Test Set Accuracy",     "On held-out test samples",            WHITE),
    ("98%",   "5-Fold Cross-Val",      "±4% variance — very stable",          GREEN),
    ("66",    "Acoustic Features",     "MFCC, pitch, RMS, ZCR, spectral...",  WHITE),
    ("51",    "Training Samples",      "11 real + 40 ElevenLabs AI voices",   WHITE),
    ("<2s",   "Detection Latency",     "End-to-end including API round-trip", GREEN),
    ("20x",   "Data Augmentation",     "Mic simulation applied to all fakes", WHITE),
]
for i, (val, lbl, sub, col) in enumerate(metrics):
    rect(s7, 7.2, 2.0+i*0.66, 5.8, 0.6, CARD, BORDER, 0.3)
    txt(s7, val, 7.35, 2.05+i*0.66, 1.2, 0.42, size=18, bold=True, color=col, font="Calibri")
    txt(s7, lbl, 8.65, 2.03+i*0.66, 2.5, 0.26, size=11, bold=True, color=WHITE)
    txt(s7, sub, 8.65, 2.3+i*0.66,  3.9, 0.26, size=9,  color=GREY)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 8 — IMPACT + CLOSING
# ─────────────────────────────────────────────────────────────────────────────
s8 = prs.slides.add_slide(BLANK)
rect(s8, 0,0,13.33,7.5, BLACK)
rect(s8, 0,0,13.33,0.06, WHITE)
rect(s8, 0,7.44,13.33,0.06, WHITE)

txt(s8, "Impact & Future", 0.6, 0.25, 6, 0.4, size=11, color=GREY)
txt(s8, "Real-World Applications", 0.6, 0.65, 10, 0.65, size=38, bold=True, color=WHITE, font="Calibri")

apps = [
    ("🏦", "Banking",       "Plug into phone banking IVR systems to flag AI-cloned authorization calls before fund transfer"),
    ("👮", "Law Enforcement","Verify audio evidence authenticity in court — detect if voice messages were AI-generated"),
    ("📱", "Messaging Apps", "WhatsApp / Telegram plugin to auto-scan incoming voice notes and warn the recipient"),
    ("🏫", "Education",      "Prevent voice impersonation in online viva, oral exams, and remote interview processes"),
    ("📰", "Media / Press",  "Journalists can verify if an audio clip from a politician or celebrity is real or deepfaked"),
    ("🔐", "Cybersecurity",  "Corporate security teams deploy as an API layer over all phone-based authentication systems"),
]
for i, (icon, title, desc) in enumerate(apps):
    col = i % 2
    row = i // 3
    lf = 0.5 + col * 6.45
    tp = 1.7 + (i % 3) * 1.6
    rect(s8, lf, tp, 6.1, 1.45, CARD, BORDER, 0.5)
    txt(s8, icon, lf+0.15, tp+0.25, 0.65, 0.9, size=26)
    txt(s8, title, lf+0.9, tp+0.2,  5.0, 0.38, size=13, bold=True, color=WHITE)
    txt(s8, desc,  lf+0.9, tp+0.62, 5.0, 0.72, size=10, color=GREY)

rect(s8, 0.5, 6.6, 12.3, 0.7, CARD, BORDER, 0.5)
txt(s8, "🎯  VoiceGuard AI  —  Built for SIH 2026  |  Team SIH26104  |  Python · Flask · scikit-learn · ElevenLabs · Cloudflare",
    0.7, 6.72, 12.0, 0.4, size=11, color=GREY, align=PP_ALIGN.CENTER)


# ── Save ────────────────────────────────────────────────────────────────────
import os
out = os.path.join(os.path.expanduser("~"), "Downloads", "VoiceGuard_AI_SIH2026.pptx")
prs.save(out)
print(f"Saved: {out}")
