# Frontend

News feed client built with Next.js. It fetches news posts from the backend and renders them in a responsive feed.

## Local development

Requires Node.js 22.23.3 (pinned in the root `.nvmrc`) and pnpm. The pnpm version is set in the `packageManager` field of the root `package.json`; an installed pnpm switches to it automatically.

1. Switch to the required Node.js version:

   ```bash
   nvm use
   ```

2. Install dependencies from the repository root (it is a pnpm workspace):

   ```bash
   pnpm install
   ```

3. Create the environment file in `apps/frontend`:

   ```bash
   cp .env.example .env
   ```

4. Start the dev server:

   ```bash
   pnpm dev
   ```

   The app will be available at http://localhost:3000. The backend must be running for the feed to load — see the [backend README](../backend/README.md).

Commands from `apps/frontend` (or from the root via `pnpm --filter frontend <command>`):

| Command | What it does |
|---|---|
| `pnpm dev` | Dev server with hot reload |
| `pnpm lint` | Lint the code with ESLint |
| `pnpm build` | Production build |
| `pnpm start` | Run the production build |

## Production build and run

The image is built from the [`Dockerfile`](Dockerfile) with the repository root as the build context: installing dependencies needs the root `package.json`, `pnpm-lock.yaml` and `pnpm-workspace.yaml`. The build has three stages:

1. **`deps`** — installs the required pnpm version via corepack, then installs dependencies strictly from the lockfile (`pnpm install --frozen-lockfile`). Application code is not copied yet, so the dependency layer stays cached when only the code changes.
2. **`build`** — copies the frontend code and runs `next build`. `NEXT_PUBLIC_BACKEND_URL` is passed as a build argument and inlined into the client bundle; the build fails if it is not set. Next.js builds the app in `standalone` mode: a minimal `server.js` bundled with only the dependencies it needs.
3. **`run`** — copies only the standalone server and the static files from `.next/static` into a clean `node:22.23.3-alpine3.24` image. The container runs as the unprivileged user `1000:1000` with `node server.js` on port `3000`.

Building and running manually (from the repository root):

```bash
docker build -f apps/frontend/Dockerfile \
  --build-arg NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 \
  -t news-frontend .
docker run -d -p 127.0.0.1:3000:3000 news-frontend
```

The backend URL is fixed at build time: rebuild the image to change it.

## Environment variables

| Variable | Used at | Default | Description |
|---|---|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | build (`next dev`, `next build`) | — | Backend URL the browser sends requests to. Must be reachable from the user's browser. Inlined into the bundle at build time; passed as a build argument in Docker |
| `PORT` | container runtime | `3000` | Standalone server port. Set in the image |
| `HOSTNAME` | container runtime | `0.0.0.0` | Interface the standalone server listens on. Set in the image |
| `NEXT_TELEMETRY_DISABLED` | container build and runtime | `1` | Disables Next.js telemetry. Set in the image |

Locally, `NEXT_PUBLIC_BACKEND_URL` is read from `apps/frontend/.env`.
