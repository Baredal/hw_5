import random
import requests
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

# URL of the client service that will receive requests
CLIENT_SERVICE = 'http://client_service:8000/invoke'

TOKEN = 'YourSuperSecretToken'

# Interval in seconds between each scheduled job
TIME_INTERVAL_SEC = 10

# Example prompts that simulate various user inputs to test the downstream model/service
prompts = [
    "HelOO woRLd",
    "TesTTT PROmpts tO ML moDEl",
    "ThiS iS a TeSt MesSaGe",
    "DoES It WorK WiTH MixEd CaSe?",
    "AnYBoDY ThErE???",
    "RuNninG lOWeRCaSe tEsts Now",
    "SenD InPuT tO tHE sErvIcE",
    "ChEcK ThE ReSpONsE QuaLiTy",
    "StrAnGe CaSe InPuT fOr YoU",
    "JuST aNOtHeR RANDoM prOMpT"
]

def trigger_client_service():
    """
    Function to send a POST request to the client service with a randomly chosen prompt.
    This simulates client input and checks whether the downstream service can handle it.
    The request is authenticated using a bearer token.
    Logs are printed for tracking.
    """
    prompt = random.choice(prompts)
    params = {
        "original_text": prompt
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.post(CLIENT_SERVICE, headers=headers, params=params)
        print(f"[Scheduler] Sent: {prompt}")
        print(f"[Scheduler] Status: {response.status_code}")

        data = response.json()
        print(f"[Scheduler] Response: {data}")

    except Exception as e:
        print(f"[Scheduler] Error sending request: {e}")

@asynccontextmanager
async def uptime(app): 
    """
    FastAPI lifespan context manager that starts a background scheduler when the app starts,
    and gracefully shuts it down when the app is terminated

    The scheduler runs the `trigger_client_service()` function at a regular interval
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(trigger_client_service, "interval", seconds=TIME_INTERVAL_SEC, max_instances=2)
    scheduler.start()
    print("[Scheduler] Started.")
    yield
    scheduler.shutdown()
    print("[Scheduler] Shutdown.")

app = FastAPI(lifespan=uptime)

@app.get("/")
async def root():
    """
    Root endpoint to verify that the scheduler service is running
    """
    return {"message": "Scheduler - triggering client service."}
