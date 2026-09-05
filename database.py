"""
VoiceGuard — SQLite Database
"""

import sqlite3
import json
from datetime import datetime
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "scans.db")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            filename     TEXT,
            status       TEXT,
            confidence   REAL,
            features_json TEXT,
            source       TEXT DEFAULT 'file_upload',
            scan_time    DATETIME
        )
    """)
    # Migrate old schema if needed
    try:
        c.execute("ALTER TABLE scans ADD COLUMN source TEXT DEFAULT 'file_upload'")
    except Exception:
        pass
    conn.commit()
    conn.close()


def log_scan(filename, status, confidence, features, source="file_upload"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO scans (filename, status, confidence, features_json, source, scan_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            status,
            round(float(confidence), 1),
            json.dumps(features),
            source,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    conn.close()


def get_recent_scans(limit=20):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT * FROM scans ORDER BY scan_time DESC LIMIT ?", (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    total = c.execute("SELECT COUNT(*) FROM scans").fetchone()[0]
    fake  = c.execute("SELECT COUNT(*) FROM scans WHERE status='FAKE'").fetchone()[0]
    real  = c.execute("SELECT COUNT(*) FROM scans WHERE status='REAL'").fetchone()[0]
    conn.close()
    return {"total": total, "fake": fake, "real": real}
