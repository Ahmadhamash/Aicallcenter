# Local Development

## Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Run tests

```bash
cd backend
pytest app/tests -q
```

## Simulate call

```bash
cd backend
PYTHONPATH=. python ../infra/scripts/mock_call_simulator.py
```
