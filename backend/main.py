from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from systems.platform_check import get_current_platform
from payment.ms_store import router as ms_router
from payment.google_play import router as google_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include both store modules
app.include_router(ms_router, prefix="/api/v1/ms")
app.include_router(google_router, prefix="/api/v1/google")

@app.post("/api/v1/buy")
async def universal_buy(plan_type: str, token: str = None):
    platform = get_current_platform()
    
    if platform == "microsoft_store":
        from payment.ms_store import process_ms_purchase
        return await process_ms_purchase(plan_type)
        
    elif platform == "google_play":
        from payment.google_play import verify_google_purchase
        if not token:
            raise HTTPException(status_code=400, detail="Missing Google Token")
        return await verify_google_purchase(token, plan_type)
        
    else:
        # Dev bypass for local testing
        from payment.ms_store import update_config
        update_config(plan_type)
        return {"status": "success", "mode": "dev_bypass"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
