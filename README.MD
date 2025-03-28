# Project Name

This project consists of several services that work together to provide a seamless flow of client requests. The services include the **Client Service**, **Database Service**, and **Business Logic Service**.

## Services Overview

### 1. **Client Service**
The Client Service handles incoming requests from clients and interacts with the other services to process and respond to those requests.
- http://localhost:8000/

### 2. **Database Service**
The Database Service is responsible for interacting with the database, handling data storage and retrieval.
- http://localhost:8002/

### 3. **Business Logic Service**
The Business Logic Service processes the data according to the application’s logic and business rules.
- http://localhost:8001/

### Prerequisites
Make sure you have the following software installed:
- Python 3.x
- Docker


## Setup and Running the Services
So start all services, copy the directory in github and in that directory run
```bash 
docker compose up
- http://localhost:8000/invoke is the main client service side, where client sends text for processing. He can not directly call methods from 8001 and 8002 ports <br>




