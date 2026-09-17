# Poth.bd (পথ) — Transit & Fare Engine

> সঠিক রুট, নির্ভুল ভাড়া — your simple journey path.

Poth.bd is a multi-modal public transit fare and route search engine for Dhaka, Bangladesh. It indexes official BRTA city bus networks and the Dhaka Metro Rail (MRT Line-6) into a single searchable database, computes distance-based fares, finds optimal transfer itineraries, and runs as an installable PWA.

---

## Table of Contents

- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Deployment](#deployment)
- [Data Sources](#data-sources)
- [License](#license)

---

## Key Features

- **Fare search** across 118 BRTA bus routes and MRT Line-6, covering 306 stops and 8,100+ fare pairs
- **Multi-modal routing** — direct bus, direct metro, and hybrid bus ↔ metro transfers
- **Fuzzy stop matching** in English and Bengali with alias resolution (e.g. `Farmgate`, `ফার্মগেট`, `mirpur 10`)
- **Metro timetable awareness** — weekday / Friday schedules from DMTCL, shown as a live operational status indicator
- **Shareable deep links** with Web Share API and clipboard fallback
- **Offline-first PWA** with Service Worker caching

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 16 (App Router), React 19, TypeScript 5, Tailwind CSS 4 |
| **Backend** | FastAPI, Python 3.11+, Pydantic v2, RapidFuzz |
| **Database** | SQLite (WAL mode) |
| **Hosting** | Frontend on Vercel, Backend on Fly.io |
| **Containerization** | Docker, Docker Compose |

---

## Prerequisites

- **Python 3.11+**
- **Node.js 22+** and npm
- Git

Docker is optional but recommended for a one-command setup.

---

## Getting Started

### Option 1: Docker Compose (Recommended)

```bash
git clone https://github.com/mahmudhas100/Poth.bd.git
cd Poth.bd
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python main.py
```

The API starts at http://localhost:8000.

#### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The app starts at http://localhost:3000.

---

## Architecture

```
Poth.bd/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/     # REST handlers: fare.py, stops.py, health.py
│   │   ├── core/              # Settings, CORS, security & rate-limit middleware
│   │   ├── db/                # SQLite connection manager (WAL, read-only pool)
│   │   ├── schemas/           # Pydantic request/response models
│   │   └── services/          # Fare engine, fuzzy stop cache, transfer router
│   ├── data/poth.db           # SQLite transit database
│   ├── tests/                 # Unit & integration tests
│   ├── Dockerfile
│   ├── fly.toml               # Fly.io production config
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js App Router (layout, page, metadata, PWA)
│   │   ├── components/        # AutocompleteInput, RouteCards, RouteSearchForm, RouteModal
│   │   ├── lib/               # API client, metro timetable engine, Google Maps resolver
│   │   └── types/             # TypeScript interfaces
│   ├── public/                # PWA manifest, icons, service worker
│   ├── Dockerfile
│   └── vercel.json
│
├── scripts/                   # Data processing, migration & normalization utilities
├── raw_data/                  # Source BRTA PDFs and extracted page images
└── docker-compose.yml
```

### Request Flow

```
User query → Next.js client → GET /search?from_stop=X&to_stop=Y → FastAPI
  → Fuzzy stop resolution (RapidFuzz, 947 cached variations)
  → Direct fare lookup + Metro fare lookup + Transfer routing
  → JSON response (FareResult | TransitResult | SuggestionResult)
→ Client renders RouteCards with fare, distance, stops, map links, metro status
```

---

## Database Schema

The SQLite database (`backend/data/poth.db`) contains:

| Table | Rows | Description |
|---|---|---|
| `stops` | 306 | Master stop/station register with English and Bengali names |
| `stop_aliases` | 302 | Search aliases, colloquial names, and landmark mappings |
| `routes` | 118 | Route definitions with mode (`bus` or `metro`) and source metadata |
| `route_stops` | 1,382 | Ordered stop sequences with cumulative distances (km) |
| `fares` | 8,121 | Fare matrix entries between stop pairs per route |

```sql
stops          (id, name_en, name_bn)
stop_aliases   (id, stop_id → stops, alias_name)
routes         (id, route_name, source_file, source_page, mode)
route_stops    (id, route_id → routes, stop_id → stops, stop_order, distance_km)
fares          (id, route_id → routes, from_stop_id → stops, to_stop_id → stops, fare_tk)
```

---

## API Reference

Base URL: `http://localhost:8000` (dev) / `https://poth-api.fly.dev` (prod)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | App status and version |
| `GET` | `/health` | Health check (exempt from rate limit) |
| `GET` | `/stops` | List all stops. Optional `?q=` filter |
| `GET` | `/search` | Fare search. Required: `?from_stop=X&to_stop=Y` |

### `GET /search` Response Types

The endpoint returns a JSON array containing one or more of:

- **`FareResult`** (`type: "direct"`) — Direct route with fare, distance, mode, intermediate stops
- **`TransitResult`** (`type: "transit"`) — Two-leg transfer with transfer point and combined fare
- **`SuggestionResult`** (`type: "suggestion"`) — Fuzzy match suggestion with corrected stop name and a nested route

### Rate Limits

| Endpoint | Limit |
|---|---|
| `/search` | 60 req/min per IP |
| All others | 120 req/min per IP |

Responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After` headers.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `DB_PATH` | No | `data/poth.db` | Path to SQLite database |
| `ENVIRONMENT` | No | `development` | `development` or `production` |
| `CORS_ORIGINS` | No | `*` | Comma-separated allowed origins |

### Frontend (`frontend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | Backend API base URL |
| `NEXT_PUBLIC_SITE_URL` | No | `https://poth.bd` | Canonical site URL for SEO |

---

## Testing

### Backend

The test suite covers health checks, stop search, fare calculations, fuzzy matching, MRT routing, hybrid transfers, security headers, input validation, and rate limiting.

```bash
cd backend
python tests/test_api.py
```

Expected output:

```
✓ test_health PASSED
✓ test_root PASSED
...
All 22/22 tests passed successfully!
```

### Frontend

```bash
cd frontend
npm run build    # TypeScript check + production build
npm run lint     # ESLint
```

---

## Deployment

### Backend → Fly.io

The backend deploys as a Docker container on Fly.io (Singapore region, `sin`).

```bash
cd backend
fly deploy
```

Configuration: [`fly.toml`](backend/fly.toml) — shared CPU, 256 MB, auto-stop/start, health check on `/health`.

### Frontend → Vercel

The frontend deploys on Vercel with zero configuration.

```bash
cd frontend
vercel --prod
```

Set `NEXT_PUBLIC_API_URL` to `https://poth-api.fly.dev` in the Vercel dashboard.

### Docker Compose (Self-Hosted)

```bash
docker-compose up --build -d
```

This runs both services behind `localhost:3000` (frontend) and `localhost:8000` (backend).

---

## Data Sources

- **BRTA** — Bus route networks, stoppage sequences, and fare matrices from official Bangladesh Road Transport Authority notifications ([brta.gov.bd](http://www.brta.gov.bd/))
- **DMTCL** — MRT Line-6 station data, fare structure, and operational timetables from Dhaka Mass Transit Company Limited ([dmtcl.gov.bd](https://dmtcl.gov.bd/))

---

## License

MIT © 2026 Poth.bd
