#  IPL Intelligence Platform

## Enterprise Cricket Analytics & Data Engineering Platform

IPL Intelligence Platform is a full-stack Data Engineering project that transforms raw IPL match data into analytical insights using modern data platform technologies.

The platform demonstrates real-world Data Engineering, Analytics Engineering, Data Warehousing, API Development, and Dashboarding practices through an end-to-end cricket analytics ecosystem.

---

#  Project Overview

This project processes historical IPL cricket data through a modern data architecture consisting of:

* Data Lake Storage
* ETL Pipelines
* Data Warehouse
* Analytics Layer
* REST APIs
* Interactive Dashboards

The goal is to simulate how enterprise-grade analytics platforms are designed and operated in production environments.

---

#  Architecture

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

#  Technology Stack

## Data Engineering

* Python
* Pandas
* PyArrow
* SQL

## Storage & Warehousing

* PostgreSQL
* MinIO Object Storage

## Orchestration

* Apache Airflow

## Analytics Engineering

* dbt

## Backend

* FastAPI
* SQLAlchemy

## Frontend

* Streamlit

## DevOps

* Docker
* Docker Compose
* Git
* GitHub

---

# 📊 Data Coverage

| Metric          | Value    |
| --------------- | -------- |
| Seasons         | 19       |
| Players         | 736      |
| Venues          | 40       |
| Matches         | 1,244    |
| Deliveries      | 250,000+ |
| Player Matchups | 31,353   |

---

#  Analytics Modules

##  Player Explorer

Analyze player performance across IPL history.

Features:

* Career Statistics
* Strike Rate Analysis
* Season Performance Trends
* Batting Intelligence

---

##  Bowler Explorer

Explore bowling performance metrics.

Features:

* Top Wicket Takers
* Economy Rate Leaders
* Bowling Performance Rankings

---

##  Matchup Intelligence

Analyze batter versus bowler rivalries.

Features:

* Head-to-Head Matchups
* Dismissal Analysis
* Rivalry Statistics

---

##  Venue Intelligence

Study venue-specific trends and scoring behavior.

Features:

* Highest Scoring Venues
* Venue Comparisons
* Historical Ground Analysis

---

##  Season Analytics

Understand league evolution over time.

Features:

* Run Trends
* Historical Season Analysis
* League Growth Insights

---

#  Data Pipeline Layers

## Bronze Layer

Raw IPL YAML files are ingested into MinIO Data Lake.

## Silver Layer

Raw data is transformed into structured parquet datasets:

* Matches
* Deliveries
* Players
* Teams
* Venues

## Gold Layer

Business-ready analytical models are created using dbt:

* Player Career Analytics
* Player Season Analytics
* Venue Analytics
* Bowling Analytics
* Matchup Intelligence
* Season Analytics

---

#  REST API

Swagger Documentation:

```text
http://localhost:8001/docs
```

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

#  Airflow Workflows

### Bronze Ingestion DAG

* Dataset ingestion
* Data Lake loading

### Silver Warehouse DAG

* Data transformation
* Warehouse loading

### Gold Analytics DAG

* dbt model execution
* Analytics refresh

---

#  Screenshots

Add screenshots here after upload:

```text
docs/screenshots/homepage.png
docs/screenshots/player_explorer.png
docs/screenshots/bowler_explorer.png
docs/screenshots/matchup_intelligence.png
docs/screenshots/venue_intelligence.png
docs/screenshots/season_analytics.png
docs/screenshots/swagger_docs.png
docs/screenshots/airflow_dag.png
```

---

#  Running Locally

Clone the repository:

```bash
git clone https://github.com/DishanGGowda/ipl-intelligence-platform.git
cd ipl-intelligence-platform
```

Start all services:

```bash
docker compose up -d
```

---

#  Service URLs

| Service              | URL                        |
| -------------------- | -------------------------- |
| Streamlit Dashboard  | http://localhost:8501      |
| FastAPI Swagger Docs | http://localhost:8001/docs |
| Airflow              | http://localhost:8080      |
| MinIO Console        | http://localhost:9001      |

---

#  Key Highlights

* End-to-End Data Engineering Pipeline
* Data Lake Architecture using MinIO
* PostgreSQL Data Warehouse
* Apache Airflow Orchestration
* dbt Analytics Engineering
* FastAPI REST APIs
* Interactive Streamlit Dashboard
* Dockerized Deployment
* Multi-Layer Data Architecture

---

# Author

**Dishan G**
