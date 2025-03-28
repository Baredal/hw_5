# Project Name

This project desings service microsystem that work together to provide a seamless flow of client requests. The services include the **Client Service**, **Database Service**, and **Business Logic Service**.

## Services Overview

### 1. **Client Service**
The Client Service handles incoming requests from clients and interacts with the other services to process and respond to those requests.
- http://localhost:8000/

### 2. **Database Service**
The Database Service is responsible for interacting with the database, handling data storage and retrieval.
- http://localhost:8002/

### 3. **Business Logic Service**
The Business Logic Service processes the data (message) to lowercase as an example of some ML operation.
- http://localhost:8001/

### Prerequisites
Make sure you have the following software installed:
- Python 3.x
- Docker

## Setup and Running the Services
So start all services, copy the directory from github repository and in that directory run
```bash 
docker compose up
```
http://localhost:8000/invoke is the main client service side, where client sends text for processing. He can not directly call methods from 8001 and 8002 ports, this is handled with token-based mechanism in coded <br>
**Client → (Client Service) → Database Service → Business Logic Service → Database Service → Client:**
1. Clients sends message through invoke
2. Database checks if already processed message exists
3. If not exist it is processing message using business service, saves into database, where key is original text and value is processed text. If message already exist, database returns saved processed result with original text.

# Usage
After you set up the project, navigate into **inference.py** file, change variable *text_to_process* to desire message (text) in str format and run file. Output will be original and processed texts

# Results
This is an example of testing endpoints from **test.py** file.
![Testing](test.png)
This is an example of what user will get after runing client service in **inference.py** file.
![Processing](inference.png)

# Notes
For more information, you can check each file, where is stored all endpoints and code. 
