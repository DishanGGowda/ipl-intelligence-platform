# 🏏 IPL Intelligence Platform

## Overview

IPL Intelligence Platform is an end-to-end Data Engineering and Analytics Engineering project built using modern data platform technologies.

The platform ingests historical IPL cricket data, processes it through a multi-layer data architecture, transforms it into analytical models, exposes insights through REST APIs, and visualizes them through interactive dashboards.

This project demonstrates real-world Data Engineering concepts including Data Lakes, ETL Pipelines, Data Warehousing, Orchestration, Analytics Engineering, API Development, and Dashboarding.

---

## Project Architecture

```text
Cricsheet IPL Dataset
            │
            ▼
     MinIO Data Lake
            │
            ▼
     Python ETL Layer
            │
            ▼
 PostgreSQL Warehouse
            │
            ▼
      dbt Models
            │
            ▼
      FastAPI APIs
            │
            ▼
 Streamlit Dashboard
```

---

## Technology Stack

### Data Engineering

* Python
* Pandas
* PyArrow
* PostgreSQL
* MinIO

### Orchestration

* Apache Airflow

### Analytics Engineering

* dbt

### API Layer

* FastAPI
* SQLAlchemy

### Visualization

* Streamlit

### DevOps

* Docker
* Docker Compose
* Git
* GitHub

---

## Data Architecture

### Bronze Layer

Raw IPL YAML files are ingested into MinIO Data Lake.

### Silver Layer

Raw data is parsed and transformed into structured parquet datasets.

Examples:

* Matches
* Deliveries
* Players
* Teams
* Venues

### Gold Layer

Business-ready analytical models are created using dbt.

Examples:

* Player Career Analytics
* Player Season Analytics
* Bowling Analytics
* Matchup Intelligence
* Venue Analytics
* Season Analytics

---

## Analytics Modules

### 👤 Player Explorer

* Career Statistics
* Strike Rate Analysis
* Season Trends
* Batting Intelligence

### 🎯 Bowler Explorer

* Top Wicket Takers
* Economy Rate Analysis
* Bowling Performance Metrics

### ⚔️ Matchup Intelligence

* Batter vs Bowler Analysis
* Rivalry Statistics
* Historical Dismissals

### 🏟️ Venue Intelligence

* Venue Scoring Patterns
* Ground Comparisons
* Venue Performance Trends

### 📈 Season Analytics

* Season Run Trends
* Historical IPL Evolution
* League Growth Analysis

---

## Data Coverage

| Metric     | Value    |
| ---------- | -------- |
| Seasons    | 19       |
| Players    | 736      |
| Venues     | 40       |
| Matches    | 1,244    |
| Deliveries | 250,000+ |
| Matchups   | 31,353   |

---

## API Endpoints

### Players

```text
/api/v1/players/top-runs
/api/v1/players/top-strike-rate
/api/v1/players/{player_name}/career
/api/v1/players/{player_name}/season-trend
```

### Bowlers

```text
/api/v1/bowlers/top-wickets
/api/v1/bowlers/best-economy
```

### Matchups

```text
/api/v1/matchups/top-rivalries/list
/api/v1/matchups/{batter_name}/{bowler_name}
```

### Venues

```text
/api/v1/venues/highest-scoring
```

### Seasons

```text
/api/v1/seasons/run-trends
/api/v1/seasons/highest-scoring
```

---

## Airflow Pipelines

### Bronze Ingestion DAG

* Dataset ingestion
* Data Lake loading

### Silver Warehouse DAG

* Data transformation
* Warehouse loading

### Gold Analytics DAG

* dbt execution
* Analytical model generation

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/DishanGGowda/ipl-intelligence-platform.git
cd ipl-intelligence-platform
```

### Start Platform

```bash
docker compose up -d
```

### Services

| Service      | URL                        |
| ------------ | -------------------------- |
| Streamlit    | http://localhost:8501      |
| FastAPI Docs | http://localhost:8001/docs |
| Airflow      | http://localhost:8080      |
| MinIO        | http://localhost:9001      |

---

## Project Highlights

* End-to-End Data Engineering Pipeline
* Data Lake Architecture using MinIO
* PostgreSQL Data Warehouse
* Apache Airflow Orchestration
* dbt Analytics Engineering
* FastAPI REST Services
* Interactive Streamlit Dashboards
* Fully Dockerized Deployment

---

## Future Enhancements

* Advanced Player Scouting Models
* Predictive Analytics
* Real-Time Match Processing
* Data Quality Monitoring
* Automated Testing Framework

---

## Author

**Dishan G**

Data Engineering Portfolio Project

IPL Intelligence Platform v1.0
