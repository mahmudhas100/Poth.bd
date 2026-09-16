# Poth.bd (পথ) — Transit & Fare Engine

> **সঠিক রুট, নির্ভুল ভাড়া — your simple journey path.**

Poth.bd is a high-performance, progressive public transit navigation system for Bangladesh. It indexes official BRTA bus routes, stop networks, and fare matrices, offering real-time fare calculations, transit transfer routing, fuzzy stop matching, and offline-first PWA support.

---

## 🌟 Features

- **Direct Route & Fare Search**: Computes official BRTA distance-based bus fares and intermediate stop breakdown.
- **Smart Transfer Routing**: Finds optimal 1-stop transfer itineraries when no direct bus connects origin and destination.
- **Fuzzy Stop Matcher**: Resolves misspelled or localized stop names instantly (e.g., `Farmgate`, `ফার্মগেট`, `mirpur 10`).
- **Share & Deep Linking**: Generates shareable URL links for routes with native Web Share API and clipboard copy fallback.
- **Offline-First PWA**: Installable app with Service Worker caching and network resilience indicators.
- **Clean Architecture**: Modular Next.js 16 frontend + async FastAPI backend with SQLite.

---

## 🏗️ Architecture

```
Poth.bd/
├── frontend/             # Next.js 16 (App Router, Tailwind CSS, TypeScript, PWA)
│   ├── src/
│   │   ├── app/          # App shell, Layouts, Page
│   │   ├── components/   # Modular UI Components (RouteCards, RouteSearchForm, Toast, Modal)
│   │   ├── lib/          # API Services & Client Utilities
│   │   └── types/        # Domain Types & Models
│   ├── public/           # PWA Manifest & Icons
│   └── Dockerfile
│
├── backend/              # FastAPI Python Microservice
│   ├── app/
│   │   ├── api/          # REST Endpoints (/search, /stops, /health)
│   │   ├── core/         # Settings & Config
│   │   ├── db/           # SQLite Connection Context Manager
│   │   ├── schemas/      # Pydantic Request/Response Models
│   │   └── services/     # Domain Logic, Fuzzy Stop Cache & Fare Math
│   ├── data/             # Bus Fare Database (busvara.db)
│   └── Dockerfile
│
└── docker-compose.yml    # Unified 1-Command Startup
```

---

## 🚀 Quick Start

### 1. Using Docker (Recommended)

Run the unified stack with a single command:

```bash
docker-compose up --build
```

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Docs (Swagger)**: `http://localhost:8000/docs`

### 2. Manual Local Setup

#### Backend (FastAPI)
```bash
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate | On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Database Schema

Poth.bd operates on a normalized SQLite schema (`data/busvara.db`):
- `stops`: Master stop register (ID, English Name, Bengali Name).
- `stop_aliases`: Normalized search variations and spelling aliases.
- `routes`: Official route definitions.
- `route_stops`: Ordered stop listings with cumulative distances (km).
- `fares`: Official fare matrices between key stop pairs.

---

## 🏛️ Data Sources & References

Route networks, stoppage sequences, and fare matrices are indexed directly from official public fare notifications and gazettes issued by the **Bangladesh Road Transport Authority (BRTA)**:
- **Official BRTA Portal**: [brta.gov.bd](http://www.brta.gov.bd/)
- **Fare Chart Notifications**: [BRTA Bus Fare Notifications & Circulars](http://www.brta.gov.bd/site/view/notices)

---

## 📄 License

MIT License © 2026 Poth.bd Team.

