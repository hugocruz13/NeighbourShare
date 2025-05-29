FROM node:18-slim as build

WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install

COPY . /app
RUN npm run build

FROM httpd:2.4

# Copiar os ficheiros de build
COPY --from=build /app/build/ /usr/local/apache2/htdocs/

# Copiar o custom.conf
COPY apache-config/custom.conf /usr/local/apache2/conf/extra/

# Incluir o custom.conf no httpd.conf
RUN echo "Include conf/extra/custom.conf" >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80
