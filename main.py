from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager

# Import custom modules
from core.ai_parser import parse_lead_data
from core.routing import init_db, route_and_save_lead


# Modern lifespan manager replacing deprecated on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⚙️ [LIFESPAN] Checking infrastructure...")
    init_db()
    yield  # Server processes requests here
    print("🛑 [LIFESPAN] Shutting down server...")


# Inject lifespan into app initialization
app = FastAPI(title="AI Lead Router API", lifespan=lifespan)


@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        # 1. Extract raw data
        payload = await request.json()
        raw_text = payload.get("raw_text", "")

        print(f"\n[📥 INCOMING LEAD] ID: {payload.get('lead_id')}")

        # 2. Brain (AI Processing)
        print("[🧠 ANALYSIS] Dispatching data to Gemini...")
        ai_analysis = parse_lead_data(raw_text, provider="gemini")

        # 3. Router
        print("[🔀 ROUTING] Processing decision...")
        decision = route_and_save_lead(payload, ai_analysis)

        print(f"[✅ DONE] Decision: {decision}")
        print("-" * 40)

        return {
            "status": "success",
            "decision": decision,
            "ai_analysis": ai_analysis
        }

    except Exception as e:
        print(f"\n[🔴 ERROR] {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    print("🚀 Starting FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)