import requests

url = "http://localhost:8000/invoke"

headers = {
    "Authorization": "Bearer YourSuperSecretToken",
    "Content-Type": "application/json"
}

params = {
    "original_text": "An EXAMPLE of MESSAGE For ML procseSING"
}

response_client_service = requests.post("http://localhost:8000/invoke", headers=headers, params=params)

print("Response from server (writes to database):", response_client_service.json())

response_health_0 = requests.get('http://localhost:8000/health')
response_health_1 = requests.get('http://localhost:8001/health')
response_health_2 = requests.get('http://localhost:8002/health')

reposnse_desc_0 = requests.get('http://localhost:8000/')
reposnse_desc_1 = requests.get('http://localhost:8001/')
reposnse_desc_2 = requests.get('http://localhost:8002/')

print("Response for health check client service:", response_health_0.json())
print("Response for health check business service:", response_health_1.json())
print("Response for health check database service:", response_health_2.json())
print("Response for description check:", reposnse_desc_0.json())
print("Response for description check:", reposnse_desc_1.json())
print("Response for description check:", reposnse_desc_2.json())


response_security_1_process = requests.post("http://localhost:8001/process", json=params, headers=headers)
print("Response for business security process check:", response_security_1_process.json())

response_security_2_write = requests.post("http://localhost:8002/write", json=params, headers=headers)
print("Response for database security write check:", response_security_2_write.json())

response_security_2_read = requests.get("http://localhost:8002/read?original_text={original_text}", headers=headers)
print("Response for database security read check:", response_security_2_read.json())

response_client_service = requests.post("http://localhost:8000/invoke", headers=headers, params=params)

print("Response from server (if already exist in database - returns original and processed texts):", response_client_service.json())