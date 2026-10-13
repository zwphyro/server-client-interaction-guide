# Backend

News feed REST API built with FastAPI. Data is stored in PostgreSQL; the database schema is managed with Alembic migrations.

All routes are served under the `/api/v1` prefix, e.g. `GET /api/v1/news-posts/`. API docs: http://localhost:8000/docs.

## Local development

Requires Python 3.13, [uv](https://docs.astral.sh/uv/) and a running PostgreSQL instance.

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create the environment file:

   ```bash
   cp .env.example .env
   ```

3. Start PostgreSQL. The easiest way is to run just this service via compose from the repository root (it uses the root `.env`, whose values must match `apps/backend/.env`):

   ```bash
   docker compose up -d postgres
   ```

4. Apply migrations:

   ```bash
   uv run task migrate-to-head
   ```

5. Start the server with auto-reload:

   ```bash
   uv run task start --dev
   ```

   The server will be available at http://localhost:8000.

`command/run.py` arguments:

| Argument | Default | Description |
|---|---|---|
| `--dev` | off | Restart the server on code changes |
| `--hostname` | `0.0.0.0` | Interface the server listens on |
| `--port` | `8000` | Server port |

### Migrations

| Command | What it does |
|---|---|
| `uv run task migrate-revision "<message>"` | Create a migration from model changes (autogenerate) |
| `uv run task migrate-to-head` | Apply all migrations |
| `uv run task migrate-to <revision>` | Upgrade to the given revision |
| `uv run task migrate-downgrade-to <revision>` | Downgrade to the given revision |
| `uv run task migrate-check-current` | Show the current database revision |
| `uv run task migrate-check-history` | Show migration history |

## Production build and run

The image is built from the [`Dockerfile`](Dockerfile) with `apps/backend` as the build context. The build has three stages:

1. **`base`** — `python:3.13.16-alpine3.24` with `/app` as the working directory.
2. **`deps`** — copies `uv` into the image and installs dependencies without the dev group (`uv sync --frozen --no-dev`) from `pyproject.toml` and `uv.lock` into `/app/.venv`. Bytecode is compiled at this stage. Application code is not copied yet, so the dependency layer stays cached when only the code changes.
3. **`run`** — copies only `.venv` and the application code (`src`, `command`, `config`, `migrations`, `alembic.ini`) into a clean base image. The container runs as the unprivileged user `1000:1000` with `python -m command.run` on port `8000`.

Migrations are not applied on server start. They run in a separate container from the same image with `alembic upgrade head` — in `docker-compose.yaml` the `backend_migrate` service does this before `backend` starts.

Building and running manually:

```bash
docker build -t news-backend apps/backend
docker run --rm --env-file apps/backend/.env news-backend alembic upgrade head
docker run -d -p 127.0.0.1:8000:8000 --env-file apps/backend/.env news-backend
```

The `.env` file is not included in the image: environment variables are passed to the container at runtime.

## Environment variables

Read from the process environment and from `apps/backend/.env`. Environment variables take precedence over the file.

| Variable | Required | Default | Description |
|---|---|---|---|
| `POSTGRES_HOST` | yes | — | PostgreSQL host |
| `POSTGRES_PORT` | yes | — | PostgreSQL port |
| `POSTGRES_DB` | yes | — | Database name |
| `POSTGRES_USER` | yes | — | Database user |
| `POSTGRES_PASSWORD` | yes | — | Database user password |
| `BACKEND_LOG_LEVEL` | yes | — | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `BACKEND_CORS_ORIGINS` | no | `["http://localhost:3000"]` | Origins allowed to make cross-origin requests. A JSON list |
