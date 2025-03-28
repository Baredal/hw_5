import requests

def check_health_statuses():
    response_health_0 = requests.get('http://localhost:8000/health')
    response_health_1 = requests.get('http://localhost:8001/health')
    response_health_2 = requests.get('http://localhost:8002/health')
    print("Response for health check client service:", response_health_0.json())
    print("Response for health check business service:", response_health_1.json())
    print("Response for health check database service:", response_health_2.json())

if __name__ == '__main__':
    check_health_statuses()
    url = "http://localhost:8000/invoke"

    headers = {
        "Authorization": "Bearer YourSuperSecretToken",
        "Content-Type": "application/json"
    }
    text_to_process = 'HEllO, wORlD' # Change here you message for server

    params = {
        "original_text": text_to_process
    }

    response_client_service = requests.post("http://localhost:8000/invoke", headers=headers, params=params)

    print("Processed message from server:", ''.join(list(response_client_service.json().values())))

