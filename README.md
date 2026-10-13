# Server-client interaction guide

A study project that demonstrates client-server interaction using a news feed as an example.

| Service | Stack | Description |
|---|---|---|
| [`apps/frontend`](apps/frontend/README.md) | Next.js, React, TypeScript | Client: the news feed |
| [`apps/backend`](apps/backend/README.md) | FastAPI, SQLAlchemy, Alembic | REST API for news posts |
| `postgres` | PostgreSQL 18 | Database |

## Running with Docker Compose

Requires Docker and Docker Compose v2.

1. Create the environment file and adjust the values if needed:

   ```bash
   cp .env.example .env
   ```

2. Build the images and start all services:

   ```bash
   docker compose up --build -d
   ```

   Services start in order: `postgres` → `backend_migrate` (applies migrations and exits) → `backend`. `frontend` does not depend on them.

3. Open:
   - frontend: http://localhost:3000
   - API: http://localhost:8000/api/v1/news-posts/
   - Swagger UI: http://localhost:8000/docs

All ports are published on `127.0.0.1` only.

Useful commands:

```bash
docker compose logs -f backend      # follow service logs
docker compose ps                   # service status
docker compose down                 # stop and remove containers
docker compose down -v              # same, and also delete database data
```

## Environment variables

Compose reads them from the `.env` file in the repository root.

| Variable | Required | Default | Description |
|---|---|---|---|
| `POSTGRES_DB` | yes | — | Database name. Used by `postgres`, `backend` and `backend_migrate` |
| `POSTGRES_USER` | yes | — | Database user |
| `POSTGRES_PASSWORD` | yes | — | Database user password |
| `POSTGRES_PORT` | no | `5432` | Host port PostgreSQL is published on. Inside the compose network the backend always connects to `postgres:5432` |
| `BACKEND_PORT` | no | `8000` | Host port the backend is published on |
| `BACKEND_LOG_LEVEL` | no | `INFO` | Backend log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `BACKEND_CORS_ORIGINS` | no | `["http://localhost:3000"]` | Origins allowed to make cross-origin requests to the backend, as a JSON list. Must include the frontend URL, so update it when changing `FRONTEND_PORT` |
| `FRONTEND_PORT` | no | `3000` | Host port the frontend is published on |
| `NEXT_PUBLIC_BACKEND_URL` | no | `http://localhost:8000` | Backend URL used by the browser. Passed to the frontend image build and inlined into the bundle, so the image must be rebuilt after changing it: `docker compose up --build -d frontend` |

`NEXT_PUBLIC_BACKEND_URL` must be reachable from the user's browser, so compose service names (e.g. `http://backend:8000`) won't work here.
