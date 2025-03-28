import time
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Business Logic Service - Processes data."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/process")
def process_data(payload: dict):
    """Simulates long-running processing (ML model, AI API call, etc.)."""

    try:
        time.sleep(3)
        processed_result = {"original": payload, "processed": True}

        return processed_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
