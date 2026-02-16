### ➡️ Full and Detailed Documentation in My Portfolio  
[Access the complete project page here](https://ferreiragabrielw.github.io/portfolio-gabriel/projetos/DataEngineering/1FitnessLLM/FitnessDataLLM.html)

# End-to-End Fitness Analytics Platform (LLM-Ready)

Production-style data engineering project transforming raw strength training and diet data into a cloud-executed, LLM-consumable analytical system.

---

##  Overview

This project implements a complete end-to-end data pipeline:

Raw CSV (Hevy + Diet)
→ Data Audit & Cleaning (Silver)
→ PostgreSQL (Amazon RDS)
→ Gold Weekly Aggregations
→ Canonical JSON Contract
→ Amazon Bedrock (Claude) Inference

The system is deterministic, idempotent, and cloud-portable.

---

##  Architecture

**Data Sources**

* Hevy workout CSV (1 row = 1 set)
* Diet daily export (SQLite → CSV)

**Data Stack**

* Python (Pandas, SQLAlchemy)
* PostgreSQL (Amazon RDS)
* Idempotent ETL pipeline
* Gold analytical views
* Canonical JSON schema (LLM-ready)
* Amazon S3 + Amazon Bedrock

---

##  ETL Characteristics

* Idempotent execution
* Explicit foreign key mapping
* Deterministic ordering
* Referential integrity enforced
* Replay-safe design

Repeated executions produce stable row counts and no duplicates.

---

## Gold Layer

Weekly aggregations include:

* Training sessions
* Total and failure sets
* Reps & load averages
* Exercise progression (week-over-week deltas)
* Diet integration
* Cycle classification

All warmups excluded by design.

---

## LLM Integration

A canonical JSON contract is generated per `week_start`, containing:

* Cycle context
* Weekly diet metrics
* Training overview
* Exercise-level metrics
* Deltas vs previous week

The JSON is uploaded to Amazon S3 and analyzed in Amazon Bedrock (Claude).

The model performs analytical reasoning only — no transformations or aggregations.

---

## AWS Execution

Run-once cloud validation:

* Amazon RDS (PostgreSQL)
* Amazon S3 (JSON artifact storage)
* Amazon Bedrock (LLM inference)

Designed for cost efficiency, but architecture supports future automation.

---

## Repository Structure

```
fitness-data-api-llm/
│
├── data/
├── etl/
├── jupyter/
├── llm/
├── quarto/
├── sql/
└── README.md
```

---

## Key Engineering Principles

* Data quality before modeling
* Deterministic aggregations
* Explicit schema contracts
* LLM-optimized structure
* Cloud portability
* Production-oriented design

---