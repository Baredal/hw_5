from fastapi import FastAPI, HTTPException, Header

db = {}
app = FastAPI()

INTERNAL_KEY = '28a3ed44e629634d618f4a52c4580f92'

def check_internal_auth(token: str = Header(None)):
    """
    Authenticate internal requests by verifying the provided authorization token.
    
    Args:
        token (str): The 'Authorization' header in the format 'Bearer <INTERNAL_KEY>'.
    
    Raises:
        HTTPException: If the token is invalid or not provided, a 403 HTTP exception is raised.
    
    Returns:
        dict: A dictionary confirming that the internal request has been authenticated.
    """
    if token != f"Bearer {INTERNAL_KEY}":
        raise HTTPException(status_code=403, detail="Unable to access database logic")
    return {"message": "Internal request authenticated"}

@app.get("/")
def root():
    """
    Root endpoint to check if the Database Service is running.

    Returns:
        dict: A message indicating the status of the service.
    """
    return {"message": "Database Service - Stores and retrieves data."}

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the service is healthy.

    Returns:
        dict: A JSON response indicating the health status of the service.
    """
    return {"status": "ok"}

@app.post("/write")
def write_data(payload: dict, authorization: str = Header(None)):
    """
    Store the original and processed (lowercased) text in the in-memory database.
    
    Args:
        payload (dict): A dictionary containing the 'original' text and 'processed' text.
        authorization (str): The 'Authorization' header expected to be in the format 'Bearer <INTERNAL_KEY>'.
    
    Raises:
        HTTPException: 
            - If the 'original' or 'processed' text is missing from the payload, a 400 HTTP exception is raised.
            - If authentication fails, a 403 HTTP exception is raised.
    
    Returns:
        dict: A message indicating the success of the data storage operation.
    """
    check_internal_auth(authorization)
    
    original_text = payload.get("original")
    processed_text = payload.get("processed")
    
    if not original_text or not processed_text:
        raise HTTPException(status_code=400, detail="Both original and processed text are required.")
    
    db[original_text] = processed_text
    return {"message": "Data saved successfully."}

@app.get("/read")
def read_data(original_text: str, authorization: str = Header(None)):
    """
    Retrieve processed data using the original text from the in-memory database.
    
    Args:
        original_text (str): The original text for which the processed text is to be retrieved.
        authorization (str): The 'Authorization' header expected to be in the format 'Bearer <INTERNAL_KEY>'.
    
    Raises:
        HTTPException: If authentication fails, a 403 HTTP exception is raised.
    
    Returns:
        dict: A dictionary containing the original text and its corresponding processed text if found, or an empty dictionary if not.
    """
    check_internal_auth(authorization)
    
    if original_text in db:
        return {original_text: db[original_text]}
    else:
        return {}
