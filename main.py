from fastapi import FastAPI, Request
import uvicorn

from core.ai_parser import parse_lead_data
from core.routing import init_db, route_and_save_lead

app = FastAPI(title="AI Lead Router API")


@app.on_event("startup")
async def startup_event():
    init_db()


@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        raw_text = payload.get("raw_text", "")

        print(f"\nID: {payload.get('lead_id')}")

        print("[Analysis] Send data in Gemini")
        ai_analysis = parse_lead_data(raw_text, provider="gemini")

        print("[Route]")
        decision = route_and_save_lead(payload, ai_analysis)

        print(f"[Done]: {decision}")
        print("-" * 40)

        return {
            "status": "success",
            "decision": decision,
            "ai_analysis": ai_analysis
        }

    except Exception as e:
        print(f"\n[Error] {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    print("Start FastAPI server on port: 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)