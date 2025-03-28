from fastapi import FastAPI, HTTPException

db = {}
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Database Service - Stores and retrieves data."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/write")
def write_data(payload: dict):
    """Writes data to the simulated database."""
    try:
        db["data"] = payload
        return {"message": "Data saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Write operation failed: {str(e)}")

@app.get("/read")
def read_data():
    """Reads data from the simulated database."""
    return db.get("data", {})
