FROM node:22.23.3-alpine3.24 AS base

WORKDIR /app

FROM base AS deps

RUN corepack enable
COPY package.json ./
RUN corepack install

COPY pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/frontend/package.json ./apps/frontend/package.json
RUN pnpm install --frozen-lockfile

FROM deps AS build

ENV NEXT_TELEMETRY_DISABLED=1

COPY apps/frontend ./apps/frontend

ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}

RUN test -n "$NEXT_PUBLIC_BACKEND_URL" \
    && pnpm --filter frontend run build \
    && rm -f apps/frontend/.next/standalone/apps/frontend/.env*

FROM node:22.23.3-alpine3.24 AS run

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

ENV PORT=3000
ENV HOSTNAME=0.0.0.0

WORKDIR /app

COPY --from=build /app/apps/frontend/.next/standalone ./
COPY --from=build /app/apps/frontend/.next/static ./apps/frontend/.next/static

RUN mkdir -p apps/frontend/.next/cache && chown -R 1000:1000 apps/frontend/.next

USER 1000:1000

WORKDIR /app/apps/frontend

EXPOSE 3000

CMD ["node", "server.js"]
