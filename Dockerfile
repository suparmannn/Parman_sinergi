# Stage 1: generate the static site into /src/dist.
FROM python:3.12-alpine AS build
WORKDIR /src
COPY build.py ./
COPY content ./content
COPY static ./static
RUN python3 build.py

# Stage 2: serve dist/ with Caddy.
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /src/dist /srv
