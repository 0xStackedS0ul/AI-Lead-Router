import sqlite3
import os
from core.notifier import send_telegram_alert

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'leads.db')

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT,
                source TEXT,
                email TEXT,
                intent TEXT,
                budget INTEGER,
                urgency TEXT,
                is_qualified BOOLEAN
            )
        ''')
        conn.commit()
    print(f"[DB INFO] База даних лідів ініціалізована.")

def route_and_save_lead(raw_payload: dict, ai_analysis: dict) -> str:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO leads (lead_id, source, email, intent, budget, urgency, is_qualified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            raw_payload.get("lead_id"),
            raw_payload.get("source"),
            raw_payload.get("contact_email"),
            ai_analysis.get("intent"),
            ai_analysis.get("budget"),
            ai_analysis.get("urgency"),
            ai_analysis.get("is_qualified")
        ))
        conn.commit()

    is_qualified = ai_analysis.get("is_qualified")
    urgency = ai_analysis.get("urgency")

    if is_qualified and urgency == "high":
        send_telegram_alert(raw_payload, ai_analysis)
        return "URGENT_ALERT_REQUIRED"
    elif is_qualified:
        return "STANDARD_FOLLOWUP"
    else:
        return "DISCARD_OR_NURTURE"