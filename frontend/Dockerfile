# Frontend Dockerfile (frontend/Dockerfile)
FROM node:18-slim

# Install dependencies
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install

# Build the React app
COPY . /app
RUN npm run build

# Serve the React app using Nginx
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
