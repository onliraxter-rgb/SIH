from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Canvas setup (16:9) ──────────────────────────────────────────────────────
W, H = 297*mm, 167*mm   # A4 landscape 16:9 approx

OUT = os.path.join(os.path.expanduser("~"), "Downloads", "VoiceGuard_AI_SIH2026.pdf")
c = canvas.Canvas(OUT, pagesize=(W, H))

# ── Palette ─────────────────────────────────────────────────────────────────
BG      = HexColor("#000000")
BG1     = HexColor("#0a0a0a")
CARD    = HexColor("#141414")
CARD2   = HexColor("#1a1a1a")
BORDER  = HexColor("#2a2a2a")
BORDER2 = HexColor("#3a3a3a")
BLACK   = HexColor("#000000")
WHITE   = HexColor("#FFFFFF")
OFFWHT  = HexColor("#E8E8E8")
GREY    = HexColor("#888888")
LGREY   = HexColor("#CCCCCC")
RED     = HexColor("#D95F4B")
DRED    = HexColor("#2a1010")
GREEN   = HexColor("#6AAB7E")
DGREEN  = HexColor("#0f2018")

# ── Helpers ──────────────────────────────────────────────────────────────────
def bg(col=BG):
    c.setFillColor(col); c.rect(0,0,W,H,fill=1,stroke=0)

def hrule(y, col=BORDER2, lw=0.5):
    c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(0, y, W, y)

def top_stripe():
    c.setFillColor(WHITE); c.rect(0, H-2, W, 2, fill=1, stroke=0)

def bot_stripe():
    c.setFillColor(WHITE); c.rect(0, 0, W, 2, fill=1, stroke=0)

def box(x, y, w, h, fill=CARD, stroke=BORDER, lw=0.5, r=4):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)

def label(text, x, y, size=9, col=GREY, font="Helvetica"):
    c.setFillColor(col); c.setFont(font, size)
    c.drawString(x, y, text)

def heading(text, x, y, size=38, col=WHITE, font="Helvetica-Bold"):
    c.setFillColor(col); c.setFont(font, size)
    c.drawString(x, y, text)

def body(text, x, y, size=12, col=LGREY, font="Helvetica", maxw=None):
    c.setFillColor(col); c.setFont(font, size)
    if maxw:
        # simple word wrap
        words = text.split()
        line = ""
        cy = y
        for w_ in words:
            test = line + (" " if line else "") + w_
            if c.stringWidth(test, font, size) > maxw:
                c.drawString(x, cy, line)
                cy -= size * 1.45
                line = w_
            else:
                line = test
        if line:
            c.drawString(x, cy, line)
        return cy
    else:
        c.drawString(x, y, text)
        return y

def chip(text, x, y, w, h=7*mm, fill=CARD, stroke=BORDER, tcol=GREY, tsize=9):
    box(x, y, w, h, fill=fill, stroke=stroke, lw=0.5)
    c.setFillColor(tcol); c.setFont("Helvetica", tsize)
    tw = c.stringWidth(text, "Helvetica", tsize)
    c.drawString(x + (w-tw)/2, y + h/2 - tsize/2.8, text)

def dot_bullet(items, x, y, size=11, gap=7*mm, col=LGREY, dot=WHITE):
    for item in items:
        c.setFillColor(dot);   c.circle(x+2, y+3.5, 1.8, fill=1, stroke=0)
        c.setFillColor(col);   c.setFont("Helvetica", size)
        c.drawString(x+7, y, item)
        y -= gap
    return y

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 1 — TITLE
# ─────────────────────────────────────────────────────────────────────────────
bg()
top_stripe(); bot_stripe()

# Left accent
c.setFillColor(WHITE); c.rect(14*mm, 40*mm, 1.2*mm, 80*mm, fill=1, stroke=0)

# Tag chip
chip("SIH 2026  ·  Team ID: SIH26104", 18*mm, 110*mm, 72*mm, 7*mm,
     tcol=GREY, tsize=9)

# Main title
c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 54)
c.drawString(18*mm, 87*mm, "VoiceGuard AI")

# White underline accent
c.setFillColor(WHITE); c.rect(18*mm, 84.5*mm, 90*mm, 1, fill=1, stroke=0)

# Subtitle
c.setFillColor(OFFWHT); c.setFont("Helvetica-Bold", 18)
c.drawString(18*mm, 76*mm, "Real-Time AI Voice Clone Detection")

# Description
c.setFillColor(GREY); c.setFont("Helvetica", 12)
c.drawString(18*mm, 67*mm, "Detect AI-cloned voices instantly — protecting people from deepfake scams,")
c.drawString(18*mm, 62*mm, "fraud calls, and voice impersonation attacks.")

# Right panel — floating card
box(195*mm, 45*mm, 86*mm, 100*mm, fill=CARD2, stroke=BORDER2, lw=0.8)
c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 36); c.drawCentredString(238*mm, 118*mm, "🎙")
c.setFillColor(GREY);  c.setFont("Helvetica", 10);    c.drawCentredString(238*mm, 112*mm, "ANALYZING VOICE...")

# Mini stat bars in right panel
stats = [("98%", "Cross-val Accuracy"), ("<2s", "Detection Speed"), ("66", "Acoustic Features")]
for i, (val, lbl) in enumerate(stats):
    sy = 95*mm - i*17*mm
    box(200*mm, sy, 76*mm, 13*mm, fill=BG1, stroke=BORDER, lw=0.4)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 14); c.drawString(205*mm, sy+4.5*mm, val)
    c.setFillColor(GREY);  c.setFont("Helvetica", 9);       c.drawString(226*mm, sy+4.5*mm, lbl)

# Bottom tech stack
c.setFillColor(BORDER2); c.rect(0, 10*mm, W, 0.3, fill=1, stroke=0)
c.setFillColor(GREY); c.setFont("Helvetica", 9.5)
c.drawCentredString(W/2, 5*mm, "Python  ·  Flask  ·  scikit-learn  ·  librosa  ·  ElevenLabs  ·  Cloudflare Tunnel")

c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 2 — PROBLEM
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("THE PROBLEM", 14*mm, H-12*mm, size=9, col=GREY)
heading("AI Voice Cloning is a", 14*mm, H-26*mm, size=36)
heading("Growing Threat", 14*mm, H-42*mm, size=36, col=RED)

c.setFillColor(LGREY); c.setFont("Helvetica", 12)
c.drawString(14*mm, H-52*mm, "Tools like ElevenLabs clone any voice from 30 seconds of audio — for free.")

threats = [
    ("📞", "Phone Scams",       '"Mom, I\'m in jail, send ₹50,000 now"',       "Fake child/relative voice targeting elderly"),
    ("🏦", "Bank Fraud",        "CEO voice cloned to authorize wire transfers",  "Criminals bypass vocal security with AI"),
    ("🎙", "Deepfake Calls",    "Fake politicians spreading disinformation",     "Fabricated audio clips go viral on social media"),
    ("👮", "Identity Theft",    "Bypassing voice authentication systems",        "Bank phone menus, workplace entry systems"),
]

cols = [14*mm, 79*mm, 144*mm, 209*mm]
for i, (icon, title, main, sub) in enumerate(threats):
    bx = cols[i]; by = 22*mm; bw = 62*mm; bh = 68*mm
    box(bx, by, bw, bh, fill=CARD, stroke=BORDER, lw=0.7)
    # Icon
    c.setFont("Helvetica-Bold", 24); c.setFillColor(WHITE)
    c.drawCentredString(bx+bw/2, by+bh-16*mm, icon)
    # Divider
    c.setFillColor(BORDER2); c.rect(bx+4*mm, by+bh-20*mm, bw-8*mm, 0.4, fill=1, stroke=0)
    # Title
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(bx+bw/2, by+bh-28*mm, title)
    # Main
    c.setFillColor(LGREY); c.setFont("Helvetica", 10)
    for j, chunk in enumerate([main[k:k+24] for k in range(0, len(main), 24)]):
        c.drawCentredString(bx+bw/2, by+bh-38*mm - j*5.5*mm, chunk)
    # Sub
    c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 9)
    for j, chunk in enumerate([sub[k:k+28] for k in range(0, len(sub), 28)]):
        c.drawCentredString(bx+bw/2, by+9*mm - j*5*mm, chunk)

# Alert banner
box(14*mm, 8*mm, W-28*mm, 11*mm, fill=DRED, stroke=RED, lw=0.8)
c.setFillColor(RED); c.setFont("Helvetica-Bold", 10)
c.drawString(18*mm, 12.5*mm, "⚠  In 2024, AI voice scams caused over $25 billion in global losses.  Detection tools are critically lacking.")
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 3 — SOLUTION
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("OUR SOLUTION", 14*mm, H-12*mm, size=9, col=GREY)
heading("VoiceGuard AI", 14*mm, H-28*mm, size=42, col=WHITE)

# 3 feature cards
features = [
    ("🎤", "Live Microphone", GREEN,
     "Speak into the mic for 5–8 seconds.", "Get instant REAL / FAKE verdict.", "Shows full acoustic breakdown."),
    ("📁", "File Upload", WHITE,
     "Upload any MP3, WAV, OGG, M4A.", "Full audio analysis in under 3s.", "Works on call recordings & voice notes."),
    ("🤖", "Scam Simulator", RED,
     "Type any scam message in text.", "ElevenLabs generates real AI clone.", "System catches it: FAKE (94%)."),
]

bw = 84*mm
for i, (icon, title, col, l1, l2, l3) in enumerate(features):
    bx = 14*mm + i*(bw+4*mm); by = 42*mm; bh = 82*mm
    box(bx, by, bw, bh, fill=CARD, stroke=BORDER, lw=0.7)
    # Coloured top bar
    box(bx, by+bh-8*mm, bw, 8*mm, fill=col, stroke=col, lw=0)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(bx+3*mm, by+bh-4.5*mm, icon+"  "+title)
    # Lines
    for j, ln in enumerate([l1, l2, l3]):
        c.setFillColor(LGREY if j < 2 else GREY)
        c.setFont("Helvetica", 11)
        c.drawString(bx+4*mm, by+bh-22*mm - j*10*mm, "→  "+ln)

# Stats row
stat_items = [("51", "Training Samples"), ("66", "Acoustic Features"),
              ("98%", "Cross-Val Score"), ("<2s", "Detection Speed"), ("3", "Input Modes")]
bh2 = 13*mm; bw2 = (W-28*mm - 4*4*mm) / 5
for i, (val, lbl) in enumerate(stat_items):
    sx = 14*mm + i*(bw2+4*mm)
    box(sx, 22*mm, bw2, bh2, fill=CARD2, stroke=BORDER2, lw=0.5)
    c.setFillColor(WHITE);  c.setFont("Helvetica-Bold", 16); c.drawCentredString(sx+bw2/2, 28.5*mm, val)
    c.setFillColor(GREY);   c.setFont("Helvetica", 9);        c.drawCentredString(sx+bw2/2, 24*mm, lbl)

c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 4 — HOW IT WORKS
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("TECHNICAL ARCHITECTURE", 14*mm, H-12*mm, size=9, col=GREY)
heading("How It Works", 14*mm, H-30*mm, size=42)

steps = [
    ("01", "Audio\nCapture", "WebM (mic) / MP3-WAV (file) / ElevenLabs API", "16 kHz mono, max 10 seconds"),
    ("02", "Feature\nExtraction", "66 acoustic features via librosa", "MFCC×40 · Pitch std · RMS std\nZCR · Spectral flatness · Chroma"),
    ("03", "ML\nClassifier", "Logistic Regression (scikit-learn)", "StandardScaler pipeline\nTrained: 11 real + 40 AI voices"),
    ("04", "Verdict &\nEvidence", "REAL ✓ or FAKE ✗ + confidence %", "Pitch variance · Dynamics\nAcoustic radar chart"),
]

sw = 64*mm; sh = 72*mm
for i, (num, title, main, detail) in enumerate(steps):
    sx = 14*mm + i*(sw+4.5*mm); sy = 30*mm
    box(sx, sy, sw, sh, fill=CARD, stroke=BORDER, lw=0.7)
    # Step number badge
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 26)
    c.drawString(sx+4*mm, sy+sh-14*mm, num)
    # Title
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 14)
    for j, ln in enumerate(title.split("\n")):
        c.drawString(sx+4*mm, sy+sh-25*mm - j*7.5*mm, ln)
    # Separator
    c.setFillColor(BORDER2); c.rect(sx+4*mm, sy+sh-43*mm, sw-8*mm, 0.4, fill=1, stroke=0)
    # Main
    c.setFillColor(LGREY); c.setFont("Helvetica", 10.5)
    body(main, sx+4*mm, sy+sh-50*mm, size=10.5, col=LGREY, maxw=sw-8*mm)
    # Detail
    c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 9.5)
    for j, ln in enumerate(detail.split("\n")):
        c.drawString(sx+4*mm, sy+11*mm - j*6*mm, ln)
    # Arrow connector
    if i < 3:
        ax = sx + sw + 1.5*mm; ay = sy + sh/2
        c.setFillColor(BORDER2); c.setFont("Helvetica-Bold", 14)
        c.drawString(ax, ay - 3, "›")

# Key insight
box(14*mm, 10*mm, W-28*mm, 15*mm, fill=DGREEN, stroke=GREEN, lw=0.8)
c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 11)
c.drawString(18*mm, 20.5*mm, "KEY INSIGHT")
c.setFillColor(LGREY); c.setFont("Helvetica", 10.5)
c.drawString(50*mm, 20.5*mm, "ElevenLabs pitch variance: 5–15 Hz  vs  Real humans: 30–80 Hz. AI sounds too perfect. The model exploits this physical gap.")
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 5 — SCIENCE / FEATURE TABLE
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("THE SCIENCE", 14*mm, H-12*mm, size=9, col=GREY)
heading("Why AI Voices Are", 14*mm, H-28*mm, size=38)
heading("Always Detectable", 14*mm, H-46*mm, size=38, col=WHITE)

# Table
headers = ["Acoustic Feature", "Real Human Voice", "ElevenLabs AI Clone"]
col_x  = [14*mm, 104*mm, 196*mm]
col_w  = [88*mm, 90*mm, 88*mm]
row_h  = 17.5*mm
start_y = H - 60*mm

# Header row
box(14*mm, start_y, W-28*mm, row_h, fill=CARD2, stroke=BORDER, lw=0.5)
for j, h_ in enumerate(headers):
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 12)
    c.drawString(col_x[j]+3*mm, start_y+6*mm, h_)

rows = [
    ("Pitch Variance (Hz std)",   "30 – 80 Hz  (emotion, stress)",      "5 – 15 Hz  (flat, robotic)"),
    ("Volume Dynamics (RMS std)", "0.05 – 0.12  (breathing, pauses)",   "0.002 – 0.01  (machine-steady)"),
    ("Spectral Flatness",         "0.01–0.04  (tonal, warm voice)",     "Higher  (synthesized noise-floor)"),
    ("MFCC Pattern",              "Irregular vocal tract shifts",         "Smooth AI-interpolated transitions"),
    ("Zero Crossing Rate",        "Variable (consonants, silence gaps)", "Uniformly smooth waveform"),
]

for i, row in enumerate(rows):
    ry = start_y - (i+1)*row_h
    fill = CARD if i%2==0 else BG1
    box(14*mm, ry, W-28*mm, row_h, fill=fill, stroke=BORDER, lw=0.3)
    c.setFillColor(OFFWHT); c.setFont("Helvetica-Bold", 11); c.drawString(col_x[0]+3*mm, ry+5.5*mm, row[0])
    c.setFillColor(GREEN);  c.setFont("Helvetica", 11);       c.drawString(col_x[1]+3*mm, ry+5.5*mm, row[1])
    c.setFillColor(RED);    c.setFont("Helvetica", 11);       c.drawString(col_x[2]+3*mm, ry+5.5*mm, row[2])

# Footer note
c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 10)
c.drawCentredString(W/2, 12*mm, "All 66 features are evaluated simultaneously — making detection robust against future AI voice improvements.")
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 6 — DEMO FLOW
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("LIVE DEMO", 14*mm, H-12*mm, size=9, col=GREY)
heading("See It In Action", 14*mm, H-30*mm, size=42)

demos = [
    ("🤖  Scam Simulator", RED,
     ["1. Open Scam Simulator tab",
      "2. Type: \"Mom, I'm in jail.",
      "   Send ₹50,000 now.\"",
      "3. Click Generate & Detect Clone",
      "4. ElevenLabs synthesizes AI voice",
      "5. System flags it immediately",
      "→ FAKE 🚨  Confidence: 94%"]),
    ("🎤  Live Microphone", GREEN,
     ["1. Open Microphone tab",
      "2. Click the mic button",
      "3. Speak naturally for 5–8 sec",
      "   (any sentence is fine)",
      "4. Click Stop, then Analyze",
      "5. Acoustic radar chart appears",
      "→ REAL ✅  Confidence: 87%+"]),
    ("📁  File Upload", WHITE,
     ["1. Open Upload Audio tab",
      "2. Drag & drop any MP3/WAV",
      "   (news clip, voice note, etc.)",
      "3. Click Analyze File",
      "4. Full MFCC breakdown shown",
      "5. Verdict delivered in <3 sec",
      "→ REAL ✅ or FAKE 🚨"]),
]

bw = 84*mm; bh = 95*mm
for i, (title, col, steps_) in enumerate(demos):
    bx = 14*mm + i*(bw+4.5*mm); by = 20*mm
    box(bx, by, bw, bh, fill=CARD, stroke=BORDER, lw=0.7)
    # Coloured header
    box(bx, by+bh-10*mm, bw, 10*mm, fill=col, stroke=col, lw=0)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 12)
    c.drawString(bx+4*mm, by+bh-5.5*mm, title)
    for j, step in enumerate(steps_):
        is_result = step.startswith("→")
        fc = col if is_result else (LGREY if not step.startswith("   ") else GREY)
        fw = "Helvetica-Bold" if is_result else "Helvetica"
        c.setFillColor(fc); c.setFont(fw, 10.5)
        c.drawString(bx+5*mm, by+bh-22*mm - j*9.5*mm, step)

c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 7 — TECH STACK + METRICS
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("TECHNOLOGY", 14*mm, H-12*mm, size=9, col=GREY)
heading("Stack & Performance", 14*mm, H-30*mm, size=42)

# LEFT: Stack
stack = [
    ("Backend",      "Python 3.10 + Flask",  "REST API, file handling, uploads, DB"),
    ("ML / Audio",   "scikit-learn + librosa","Logistic Regression · 66 acoustic features"),
    ("Voice Synth",  "ElevenLabs REST API",   "Generates real AI clones for the simulator"),
    ("Live Audio",   "Web Audio API",          "Real-time waveform + MediaRecorder mic"),
    ("Database",     "SQLite",                 "Scan history, stats, confidence logs"),
    ("Hosting",      "Cloudflare Tunnel",       "Live public URL, zero port-forwarding setup"),
]

for i, (lbl, tech, desc) in enumerate(stack):
    sy = H-50*mm - i*16*mm
    box(14*mm, sy, 128*mm, 14*mm, fill=CARD, stroke=BORDER, lw=0.4)
    c.setFillColor(GREY);  c.setFont("Helvetica", 9);        c.drawString(17*mm, sy+5.5*mm, lbl.upper())
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 11);  c.drawString(45*mm, sy+5.5*mm, tech)
    c.setFillColor(LGREY); c.setFont("Helvetica", 10);       c.drawString(100*mm, sy+5.5*mm, "·  "+desc)

# RIGHT: Metrics
metrics = [
    ("100%",  "Test Set Accuracy",     "Held-out test samples",              WHITE),
    ("98%",   "5-Fold Cross-Val",      "Variance: ±4%  — very stable",       GREEN),
    ("51",    "Training Samples",      "11 real humans + 40 ElevenLabs AI",  WHITE),
    ("66",    "Acoustic Features",     "MFCC, pitch, RMS, ZCR, chroma...",   WHITE),
    ("<2s",   "Detection Latency",     "End-to-end including API response",  GREEN),
    ("20×",   "Data Augmentation",     "Mic simulation applied to all fakes",WHITE),
]

mw = 130*mm
for i, (val, lbl, sub, col) in enumerate(metrics):
    my = H-50*mm - i*16*mm
    box(150*mm, my, mw, 14*mm, fill=CARD, stroke=BORDER, lw=0.4)
    c.setFillColor(col);   c.setFont("Helvetica-Bold", 16); c.drawString(154*mm, my+4.5*mm, val)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 11); c.drawString(178*mm, my+7*mm, lbl)
    c.setFillColor(GREY);  c.setFont("Helvetica", 9.5);     c.drawString(178*mm, my+2*mm, sub)

c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 8 — IMPACT & CLOSING
# ─────────────────────────────────────────────────────────────────────────────
bg(); top_stripe(); bot_stripe()

label("REAL-WORLD IMPACT", 14*mm, H-12*mm, size=9, col=GREY)
heading("Applications", 14*mm, H-30*mm, size=42)

apps = [
    ("🏦", "Banking & Finance",   "Plug into IVR phone systems to flag AI-cloned\nauthorization calls before fund transfers."),
    ("👮", "Law Enforcement",     "Verify audio evidence authenticity in court.\nDetect AI-fabricated voice recordings."),
    ("📱", "Messaging Platforms", "WhatsApp / Telegram plugin to auto-scan\nincoming voice notes and warn users."),
    ("🏫", "Online Education",    "Prevent voice impersonation in oral exams,\nviva voce, and remote interviews."),
    ("📰", "Media & Journalism",  "Verify if audio clips from politicians or\ncelebrities are real or deepfaked."),
    ("🔐", "Enterprise Security", "Deploy as API layer over phone-based\ncorporate authentication systems."),
]

aw = (W - 28*mm - 2*4*mm) / 3
ah = 48*mm
for i, (icon, title, desc) in enumerate(apps):
    col_ = i % 3; row_ = i // 3
    ax = 14*mm + col_*(aw+4*mm)
    ay = H - 50*mm - row_*(ah+5*mm)
    box(ax, ay, aw, ah, fill=CARD, stroke=BORDER, lw=0.6)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 18); c.drawString(ax+4*mm, ay+ah-12*mm, icon)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 12); c.drawString(ax+16*mm, ay+ah-11*mm, title)
    c.setFillColor(GREY);  c.setFont("Helvetica", 10)
    for j, ln in enumerate(desc.split("\n")):
        c.drawString(ax+4*mm, ay+ah-24*mm - j*7*mm, ln)

# Closing bar
box(14*mm, 8*mm, W-28*mm, 12*mm, fill=CARD2, stroke=BORDER2, lw=0.6)
c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 13)
c.drawCentredString(W/2, 13.5*mm, "VoiceGuard AI  —  Smart India Hackathon 2026  |  SIH26104")
c.setFillColor(GREY); c.setFont("Helvetica", 10)
c.drawCentredString(W/2, 9.5*mm, "Python · Flask · scikit-learn · librosa · ElevenLabs · Cloudflare")

c.showPage()

# ── Save ─────────────────────────────────────────────────────────────────────
c.save()
print(f"Saved to: {OUT}")
