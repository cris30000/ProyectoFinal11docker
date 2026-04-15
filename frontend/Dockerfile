FROM node:22-alpine AS builder

WORKDIR /app

# Copiar archivos de configuración
COPY package*.json ./
RUN npm ci

# Copiar código fuente y construir
COPY . .
RUN npm run build

# Usar nginx para servir la aplicación
FROM nginx:alpine

# Copiar los archivos construidos
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de nginx
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    try_files $uri $uri/ /index.html; \
    } \
    location /api { \
    proxy_pass http://backend:8000; \
    proxy_set_header Host $host; \
    proxy_set_header X-Real-IP $remote_addr; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]