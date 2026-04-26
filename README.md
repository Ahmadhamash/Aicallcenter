# AI Call Center SaaS for Restaurants

Multi-tenant Arabic-first AI voice ordering platform using OpenAI Realtime API with telephony abstraction.

## Monorepo structure

- `backend/`: FastAPI backend, realtime bridge, domain services, order state machine.
- `frontend/`: Next.js dashboards for Agent / Restaurant Owner / Admin.
- `infra/`: Docker Compose and helper scripts.
- `docs/`: Architecture and operational guidance.

## Quick start

1. Copy env files:
   - `cp backend/.env.example backend/.env`
   - `cp frontend/.env.example frontend/.env.local`
2. Start stack: `docker compose -f infra/docker-compose.yml up --build`
3. Run migrations: `docker compose exec backend alembic upgrade head`
4. Seed sample restaurant: `docker compose exec backend python -m app.db.seed`

## Core capabilities

- Arabic (Jordanian dialect first) conversational ordering.
- Realtime audio bridge with OpenAI Realtime WebSocket.
- Event-driven call orchestration and order state machine.
- Escalation/handoff rules for safety and low-confidence handling.
- Role-based SaaS dashboards (agent / owner / admin).

See `docs/architecture.md` for full design.
