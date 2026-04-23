import requests

WEBHOOK_URL = "http://127.0.0.1:8000/webhook"

mock_lead_data = {
    "lead_id": "L-99812",
    "source": "landing_page",
    "raw_text": "Hi, I urgently need to automate the backend for my company. The budget is around $1,500, but we need to get started tomorrow.",
    "contact_email": "client@example.com"
}

print(f"Sending a test webhook to {WEBHOOK_URL}")

try:
    response = requests.post(WEBHOOK_URL, json=mock_lead_data)
    print(f"Server response status: {response.status_code}")
    print(f"Text of the reply: {response.json()}")

except requests.exceptions.ConnectionError:
    print("[ERROR] Unable to connect. Please ensure that main.py is currently running!")