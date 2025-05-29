# Dockerfile
FROM python:3.12-slim-bookworm

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    curl gnupg ca-certificates apt-transport-https wget \
    unixodbc-dev gcc g++ \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Adiciona o repositório da Microsoft
RUN wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb

# Instala o driver ODBC da Microsoft
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código da app
COPY . /app
WORKDIR /app

# Expõe a porta onde o FastAPI irá correr
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
