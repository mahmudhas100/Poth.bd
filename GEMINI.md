# Bus Vara Project Context

## Project Overview
Automating bus fare data extraction from BRTA PDF fare charts into a structured SQLite database and serving it via a FastAPI backend.

## Project Structure
- `app/`: FastAPI application (Phase 2)
- `data/`: Final database (`poth.db`) and normalized stop data
- `scripts/`: Data processing, normalization, and migration scripts
- `raw_data/`: Original PDFs and extracted page images

## Bus Fare Data Extraction Protocols
- **JSON Structure**: Strictly follow the existing JSON structure during extraction.
- **Validation**:
    - Carefully double-check for syntax errors in fare matrices.
    - ALWAYS run a JSON validation script after writing each batch file:
      `python -c "import json; json.load(open('path/to/file.json', encoding='utf-8'))"`

## Core References
- Database: `data/poth.db`
- Master Stops: `data/master_stops.json`
