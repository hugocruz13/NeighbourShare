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


