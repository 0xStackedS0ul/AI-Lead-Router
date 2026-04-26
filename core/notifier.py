import os
import requests
from dotenv import load_dotenv

# Завантажуємо ключі
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(lead_data: dict, ai_analysis: dict):
    """
    Відправляє структуроване HTML-повідомлення в Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARNING] Telegram credentials missing. Alert not sent.")
        return

    # Форматуємо красиве повідомлення
    message = (
        f"🚨 <b>URGENT LEAD ALERT</b> 🚨\n\n"
        f"👤 <b>Email:</b> {lead_data.get('contact_email', 'N/A')}\n"
        f"🎯 <b>Intent:</b> {ai_analysis.get('intent')}\n"
        f"💰 <b>Budget:</b> ${ai_analysis.get('budget', 'N/A')}\n"
        f"⚡ <b>Urgency:</b> {ai_analysis.get('urgency').upper()}\n\n"
        f"📝 <b>Raw Text:</b>\n<i>{lead_data.get('raw_text')}</i>"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[🚀 NOTIFIER] Telegram alert sent successfully!")
        else:
            print(f"[🔴 NOTIFIER ERROR] Failed to send: {response.text}")
    except Exception as e:
        print(f"[🔴 NOTIFIER ERROR] Connection failed: {e}")