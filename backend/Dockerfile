# Dockerfile
FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    curl gnupg apt-transport-https \
    unixodbc-dev gcc g++ \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Adiciona o repositório da Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instala o driver ODBC da Microsoft
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql17 \
    && apt-get clean

# Instala dependências Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código da app
COPY . /app
WORKDIR /app

# Expõe a porta onde o FastAPI irá correr
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]
