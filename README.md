# MVV Pipeline — Real-time Train Delay Analytics

An end-to-end data engineering pipeline that collects real-time train delay data from Deutsche Bahn's API, transforms it through a medallion architecture, and visualizes insights in an interactive dashboard.

## Architecture

```
DB Timetables API
↓
Bronze Layer (Raw XML)
↓
Silver Layer (Parsed JSON)
↓
Gold Layer (DuckDB + dbt)
↓
Streamlit Dashboard
```

## Tech Stack

- **Ingestion** — Python, Requests
- **Orchestration** — Apache Airflow (Astro)
- **Storage** — Local filesystem (Bronze/Silver), DuckDB (Gold)
- **Transformation** — Python, dbt
- **Dashboard** — Streamlit
- **Environment** — uv, Docker


## Project Structure

```
mvv-pipeline/
├── ingestion/          # API extraction and data loading
├── transformation/     # Data transformation and joining
├── dashboard/          # Streamlit dashboard
├── orchestration/      # Airflow DAGs
├── transformation_dbt/ # dbt models (Gold layer)
├── data/
│   ├── raw/           # Bronze layer (XML)
│   └── transformed/   # Silver layer (JSON)
└── utils/             # Logging utilities
```