from fastapi import FastAPI, Header, HTTPException
import requests
import os

APP_TOKEN =  "YourSuperSecretToken"

DB_SERVICE_URL = "http://database_service:8002"
BUSINESS_SERVICE_URL = "http://business_service:8001"


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Client Service - Gateway to the microservices."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/process")
def process_request(authorization: str = Header(None)):
    """Handles the main workflow: fetch -> process -> store -> return result."""
    
    if authorization != f"Bearer {APP_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        db_response = requests.get(f"{DB_SERVICE_URL}/read")
        db_response.raise_for_status()
        data = db_response.json()

        if not data:
            raise HTTPException(status_code=404, detail="No data available in the database.")


        process_response = requests.post(f"{BUSINESS_SERVICE_URL}/process", json=data)
        process_response.raise_for_status()
        processed_data = process_response.json()

        write_response = requests.post(f"{DB_SERVICE_URL}/write", json=processed_data)
        write_response.raise_for_status()

        return processed_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Service request failed: {str(e)}")



