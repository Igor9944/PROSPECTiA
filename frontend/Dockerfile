# Build stage
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .

# VITE_API_URL fourni par Railway au build (Variables)
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL
ENV GITHUB_PAGES=false

RUN npm run build

# Serve stage — Caddy pour le routing SPA
FROM caddy:2-alpine
WORKDIR /srv

COPY --from=build /app/dist /srv
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 3000
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
