# NeighbourShare

  NeighbourShare é um projeto prático desenvolvido para as unidades curriculares de **PDS (Projeto de Desenvolvimento de Software)** e **Programação Web**. O objetivo deste projeto é criar uma aplicação colaborativa que permite aos utilizadores compartilhar e solicitar recursos dos seus vizinhos, promovendo a cooperação e o senso de comunidade.
  
## Running the Project with Docker Compose

### Prerequisites

- Docker installed and running on your machine. You can download it here: [Docker Desktop](https://www.docker.com/products/docker-desktop)  
### Steps to run the project

1. Open a terminal inside the project root directory (where the `docker-compose.yml` file is located).
2. Run the following command to build and start all containers (database, backend, frontend):

```bash
docker-compose up --build
```

3. Access the application at:
	- Frontend: [http://localhost](http://localhost) (port 80)
	- Backend API: [http://localhost:8000](http://localhost:8000)
    - SQL Server Database: connect using port 1433 (`localhost,1433`) with the following credentials:
        - Username: `sa`  
	    - Password: `DEVesi2025`
        - Database: `NeighbourShare`
4. To stop and remove the containers:
```bash
docker-compose down
```
## Running the Backend 

1. Make sure you have your `.env` file set up (saved as `2024_2025` or as needed).
2. Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

- On **Linux/macOS**:
```bash
source .venv/bin/activate
```

- On **Windows (PowerShell)**:
```powershell
.\.venv\Scripts\Activate.ps1
```    

- On **Windows (bash)**:
```bash
source .venv/Scripts/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend API:
```bash
uvicorn main:app --reload
```

## Running Tests

1. Pull the test database image (optional if you use Docker for the DB tests):
```bash
docker pull ghcr.io/hugocruz13/neighbourshare-db:tests
```
2. Inside the `backend` folder, activate your virtual environment (same as above).
3. Run the tests with pytest:
```bash
pytest tests/test_anr.py
```

## Running the Frontend 

1. Install the project dependencies:
```bash
npm install
```

2. Start the frontend development server:
```bash
npm start
```

3. Open your browser and navigate to:  
   [http://localhost:3000](http://localhost:3000)
   
> **Note:** By default, React runs on port 3000. If port 3000 is busy or configured differently, check your terminal output for the actual URL.
