import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from google import genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a strict AI lead qualifier. 
Your task is to extract information from the client’s text and return ONLY valid JSON.
The JSON format must be strictly as follows:
{
    "intent": "short description in English",
    "budget": number (or null),
    "urgency": "low", "medium" або "high",
    "is_qualified": true або false
}
No further words or explanations.
"""

#GEMINI
def parse_with_gemini(raw_text: str) -> dict:
    if not GEMINI_API_KEY:
        print("[ERROR] Not found GEMINI_API_KEY")
        return {}

    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{raw_text}",
            config={
                "temperature": 0.0,
                "response_mime_type": "application/json"
            }
        )

        return json.loads(response.text)

    except Exception as e:
        print(f"[ERROR] ERROR Gemini API: {e}")
        return {}


#OPENAI
def parse_with_openai(raw_text: str) -> dict:
    if not OPENAI_API_KEY:
        print("[ERROR] Not found OPENAI_API_KEY")
        return {}

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_text}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"[ERROR] ERROR OpenAI API: {e}")
        return {}


#ORCHESTRATOR
def parse_lead_data(raw_text: str, provider: str = "gemini") -> dict:
    if provider == "gemini":
        return parse_with_gemini(raw_text)
    elif provider == "openai":
        return parse_with_openai(raw_text)
    else:
        print(f"[ERROR] Unknown provider: {provider}")
        return {}


#TEST
if __name__ == "__main__":
    print("AI Parser...\n")

    test_text = "Hi, I urgently need to automate the backend for my company. The budget is around $1,500, but we need to get started tomorrow."
    print(f"Input text: {test_text}\n")

    parsed_result = parse_lead_data(test_text, provider="gemini")

    print("[ANALYSIS RESULTS]")
    print(json.dumps(parsed_result, indent=4, ensure_ascii=False))