from fastapi import FastAPI, Header, HTTPException
import requests

APP_TOKEN = "YourSuperSecretToken"
DB_SERVICE_URL = "http://database_service:8002"
BUSINESS_SERVICE_URL = "http://business_service:8001"
INTERNAL_BUSINESS_KEY = '4830395c22cf1dc8405b83c399ed9edd'
INTERNAL_DB_KEY = '28a3ed44e629634d618f4a52c4580f92'

app = FastAPI()

@app.get("/")
def root():
    """
    Root endpoint to check if the Client Service is running.

    Returns:
        dict: A message indicating the status of the service.
    """
    return {"message": "Client Service - Gateway to the microservices."}

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the service is healthy.

    Returns:
        dict: A JSON response indicating the health status of the service.
    """
    return {"status": "ok"}

@app.post("/invoke")
def process_request(original_text: str, authorization: str = Header(None)):
    """
    Handles the main workflow: fetch -> process -> store -> return result.
    
    This endpoint interacts with the Database Service and Business Logic Service in sequence:
    1. It first checks if the requested data exists in the database.
    2. If the data is not found, it triggers the Business Logic Service to process the data.
    3. Once the data is processed, it is stored in the database.
    4. Finally, the processed data is returned.
    
    Args:
        original_text (str): The original text to be processed.
        authorization (str): The 'Authorization' header expected to be in the format 'Bearer <APP_TOKEN>'.
    
    Raises:
        HTTPException: 
            - If the authorization token is invalid, a 401 Unauthorized exception is raised.
            - If any service request fails, a 500 Internal Server Error exception is raised.
    
    Returns:
        dict: The processed data, either retrieved from the database or newly processed by the Business Logic Service.
    """
    if authorization != f"Bearer {APP_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        db_response = requests.get(f"{DB_SERVICE_URL}/read", params={"original_text": original_text}, headers={"Authorization": f"Bearer {INTERNAL_DB_KEY}"})
        db_response.raise_for_status()
        data = db_response.json()

        if not data:
            process_response = requests.post(f"{BUSINESS_SERVICE_URL}/process", json={"original": original_text}, headers={"Authorization": f"Bearer {INTERNAL_BUSINESS_KEY}"})
            process_response.raise_for_status()
            processed_data = process_response.json()

            write_response = requests.post(f"{DB_SERVICE_URL}/write", json=processed_data, headers={"Authorization": f"Bearer {INTERNAL_DB_KEY}"})
            write_response.raise_for_status()
            
            return processed_data
        else:
            return data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Service request failed: {str(e)}")
