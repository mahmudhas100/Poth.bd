# Poth.bd (পথ) — Transit & Fare Engine

> **সঠিক রুট, নির্ভুল ভাড়া — your multi-modal journey companion for Dhaka.**

Poth.bd is a high-performance, multi-modal public transit routing engine for Dhaka. It seamlessly integrates official BRTA city bus routes, the Dhaka Metro Rail (MRT Line-6 / DMTCL), real-time operational timetable awareness, hybrid transfers, and fuzzy stop search into a responsive, offline-ready progressive web app.

---

## 🌟 Key Capabilities

- **Multi-Modal Transit Routing**: Queries direct bus routes, direct Dhaka Metro Rail (MRT Line-6), and hybrid multimodal transfers (Metro + Bus) with preference ranking and transfer-time penalties.
- **Directional DMTCL Metro Timetable Engine**:
  - Full operational schedule parsing matching official DMTCL guidelines.
  - Distinguishes weekday vs. Friday operational profiles, peak vs. off-peak intervals (5–12 mins), and extended services (up to 22:46) for MRT/Rapid Pass holders.
  - Real-time subtle operational status indicators (live status dot with active headway and operating window).
- **Intelligent Stop Resolution & Search**:
  - Real-time fuzzy Bengali & English search with sub-string and transliteration matching.
  - Distinct emerald **M** badge beside Metro Rail stations in autocomplete results.
  - Landmark aliasing (e.g. *Secretariat (Paltan)* aliased to *Paltan*, *Bahadur Shah Park* aliased to *Sadarghat*).
- **Disambiguated Map Navigation**:
  - Deep-linked Google Maps routing with station-specific POI resolution (e.g., appending "Metro Station" or landmark anchors) to eliminate map pin ambiguities.
- **Offline-First PWA**:
  - Installable progressive web application with Service Worker caching and network resilience indicators.
- **Clean Microservice Architecture**:
  - Next.js 16 (React 19, Turbopack, Tailwind CSS, TypeScript) paired with an async FastAPI backend running SQLite with WAL-mode concurrency.

---

## 🏗️ Architecture

```
Poth.bd/
├── frontend/             # Next.js 16 (App Router, Tailwind CSS, TypeScript, PWA)
│   ├── src/
│   │   ├── app/          # App Shell, Routing, Layouts, Metadata
│   │   ├── components/   # UI Components (AutocompleteInput, RouteCards, RouteSearchForm, Modal)
│   │   ├── lib/          # API Client, DMTCL Metro Timetable Engine, Maps POI Resolvers
│   │   └── types/        # TypeScript Interfaces & Multi-Modal Transit Contracts
│   ├── public/           # PWA Manifest, Icons & Service Worker
│   └── Dockerfile
│
├── backend/              # FastAPI Python Microservice
│   ├── app/
│   │   ├── api/          # REST Endpoints (/search, /stops, /health)
│   │   ├── core/         # Settings, Security Middleware & Concurrency Setup
│   │   ├── db/           # SQLite Session Context Manager (WAL Mode, Read-Only pool)
│   │   ├── schemas/      # Pydantic v2 Request/Response Validation Models
│   │   └── services/     # Multi-Modal Routing Engine, Fuzzy Stop Cache & Fare Math
│   ├── data/             # Normalized Transit Database (poth.db)
│   ├── tests/            # Automated Unit & Integration Test Suite
│   ├── Dockerfile
│   └── fly.toml          # Fly.io Production Configuration
│
└── docker-compose.yml    # Unified 1-Command Startup
```

---

## 🚀 Quick Start

### 1. Using Docker (Recommended)

Run the entire stack with Docker Compose:

```bash
docker-compose up --build
```

- **Frontend App**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

### 2. Manual Local Development

#### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Run test suite:
```bash
python tests/test_api.py
```

#### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

Production build:
```bash
npm run build
```

---

## 📊 Database Architecture

Poth.bd operates on a normalized SQLite schema (`backend/data/poth.db`):
- `stops`: Master stop and station register (ID, English Name, Bengali Name).
- `stop_aliases`: Search variations, colloquial names, and station landmark aliases.
- `routes`: Official route definitions, mode identifiers (`bus`, `metro`), and operator details.
- `route_stops`: Sequential stoppage orders with cumulative point-to-point distances (km).
- `fares`: Distance-based fare matrices and flat fare mappings across stop pairs.

---

## 🏛️ Official Data References

Transit networks, stoppage sequences, and fare calculations are indexed from official notifications:
- **BRTA (Bangladesh Road Transport Authority)**: Official city bus fare gazettes and stoppage notifications ([brta.gov.bd](http://www.brta.gov.bd/)).
- **DMTCL (Dhaka Mass Transit Company Limited)**: Dhaka Metro Rail MRT Line-6 operational guidelines, station matrix, and timetable circulars ([dmtcl.gov.bd](https://dmtcl.gov.bd/)).

---

## 📄 License

MIT License © 2026 Poth.bd Team.
