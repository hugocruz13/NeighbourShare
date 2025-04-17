# Frontend Dockerfile (frontend/Dockerfile)
FROM node:18-slim as build

# Install dependencies
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install

# Build the React app
COPY . /app
RUN npm run build

# Segunda etapa com Apache
FROM httpd:2.4

# Copiar os arquivos de build do React para o diretório do Apache
COPY --from=build /app/build/ /usr/local/apache2/htdocs/

# Copiar arquivo de configuração personalizado do Apache
#COPY httpd.conf /usr/local/apache2/conf/httpd.conf

# Expor a porta 80
EXPOSE 80

RUN echo "Include conf/extra/custom.conf" >> /usr/local/apache2/conf/httpd.conf