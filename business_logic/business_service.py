from fastapi import FastAPI, HTTPException, Header

app = FastAPI()

INTERNAL_KEY = '4830395c22cf1dc8405b83c399ed9edd'

def check_internal_auth(token: str = Header(None)):
    """
    Authenticate internal requests to ensure that the request has the correct authorization token.
    
    Args:
        token (str): The authorization token passed in the request header.
    
    Raises:
        HTTPException: If the token doesn't match the INTERNAL_KEY, a 403 Forbidden error is raised.
    
    Returns:
        dict: A message confirming successful authentication if the token is valid.
    """
    if token != f"Bearer {INTERNAL_KEY}":
        raise HTTPException(status_code=403, detail="Unable to access business logic")
    return {"message": "Internal request authenticated"}

@app.get("/")
def root():
    """
    Root endpoint to indicate that the Business Logic Service is running.
    
    Returns:
        dict: A message indicating the status of the service.
    """
    return {"message": "Business Logic Service - Processes data."}

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the service's health.
    
    Returns:
        dict: A JSON response indicating the health status of the service.
    """
    return {"status": "ok"}

@app.post("/process")
def process_data(text: dict, authorization: str = Header(None)):
    """
    Simulate processing of data by converting the provided text to lowercase.
    
    This endpoint receives a JSON object containing text, and returns the same text but in lowercase.
    
    Args:
        text (dict): The request body containing the 'original' text to be processed.
        authorization (str): The 'Authorization' header expected to be in the format 'Bearer <INTERNAL_KEY>'.
    
    Raises:
        HTTPException: 
            - If the authorization token is invalid, a 403 Forbidden exception is raised.
            - If the 'original' text is not provided in the request body, a 400 Bad Request exception is raised.
    
    Returns:
        dict: A JSON response containing both the original text and the processed (lowercased) text.
    """
    check_internal_auth(authorization)
    
    original_text = text.get("original")
    if not original_text:
        raise HTTPException(status_code=400, detail="Original text is required in the input.")
    
    processed_text = original_text.lower()

    return {"original": original_text, "processed": processed_text}
