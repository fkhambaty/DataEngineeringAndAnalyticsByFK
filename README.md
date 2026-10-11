# Data Engineering & Analytics by FK: Meridian Bank end-to-end project

A production-shaped teaching/reference platform for a fictional multi-country bank (**Meridian Bank**,
520 branches, 5 currencies, retail banking plus credit cards). Built with Postgres →
Python → Snowflake → dbt → Airflow, with ML decisioning, a governed plain-English app,
platform-as-code, and a performance lab where things are made slow on purpose and then
fixed with measured before/after numbers.

It is designed to be built and defended the way an architect would, not just run:
every hard-to-reverse choice has a written decision record, and every number in the
design doc can be recomputed.

Public source for students: <https://github.com/fkhambaty/DataEngineeringAndAnalyticsByFK>

The lessons, decks, and dry run are in this repository. The same pipeline as code only, ready to clone and run, is <https://github.com/fkhambaty/snowflake_dbt_airflow_python_byFK>.

**Start here:**
1. [`00_architecture/DESIGN_DOC.md`](00_architecture/DESIGN_DOC.md): requirements, SLOs, capacity and cost math, data classification, failure modes.
2. [`00_architecture/ARCHITECTURE_PROCESS.md`](00_architecture/ARCHITECTURE_PROCESS.md): requirements-to-operations design sequence and standard artifacts.
3. [`course/index.html`](course/index.html) (open in a browser): the episode list. Each video links to the animated presentation, the written code lesson, and the dry run where one exists.
4. [`00_architecture/OPERATIONS_RUNBOOK.md`](00_architecture/OPERATIONS_RUNBOOK.md) and [`00_architecture/DR_RUNBOOK.md`](00_architecture/DR_RUNBOOK.md): incident and recovery procedures.

## Folder map (follow in this order)

| Folder | What it is | Run with |
|---|---|---|
| `course/` | Episode list, animated decks, written guide, dry run | open `course/index.html` |
| `00_architecture/` | Design doc, the architecture process (which diagram at which step), and Architecture Decision Records | read first |
| `01_source_postgres/` | OLTP schema (3NF), SQL seed scripts (520 branches, 200k customers, 5M+ transactions, cards), CDC triggers, DML simulator procedures | `psql` |
| `02_ingestion_python/` | Beginner foundations in `00_python_foundations/`, then micro-batch Postgres → Parquet → Snowflake ingestion, simulation, and source-to-warehouse reconciliation with pandas | `python3` |
| `03_snowflake/` | Account bootstrap, RBAC, raw/control tables, operations and cost views, Time Travel/clone DR exercise, row access + tag-based masking | Snowsight |
| `04_dbt_meridian_dw/` | dbt: sources + freshness, staging, SCD2, Kimball marts, three public contracts, incremental/unit proofs, exposures, governance hooks | `dbt build` |
| `05_airflow/` | Astro/Airflow: pooled 5-minute hot path, daily reference batch, decisioning, freshness watchdog, bounded replay | `astro dev start` |
| `06_performance_lab/` | Deliberately slow scenarios + fixes + measurement queries (Postgres and Snowflake) | `psql` / Snowsight |
| `07_data_modelling/` | Bus matrix, ERD and star schema sources (Mermaid) | any Mermaid renderer |
| `.github/workflows/` | Active offline checks and Snowflake slim-CI workflows; `08_ci_cd/` documents their design | GitHub |
| `09_decisioning_python/` | Card decision, propensity and fraud models trained from gold features; AUC gate; writes `MERIDIAN_RAW.ML` | `python3` |
| `10_semantic_app/` | Snowflake semantic view + Streamlit/Cortex Analyst app. Login is a Snowflake user; row policies limit the answer | Snowsight, or `streamlit run` |
| `11_platform_terraform/` | The same roles, warehouses, resource monitor and databases as `03_snowflake/01–02`, as Terraform | `terraform plan` |
| `tests/` | pytest for the Python logic that must hold without a warehouse | `pytest` |

## Quick start (local)

New machine? Follow [`setup/README.md`](setup/README.md). It contains the macOS and
Windows installers, a setup verifier, and the automated PostgreSQL build.

```bash
# 0. Verify the local tools, then build the complete source database.
python3 setup/verify_setup.py
python3 setup/start_postgres.py

# 1. Python deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pytest

# New to Python? Run the four small lessons first.
python3 02_ingestion_python/00_python_foundations/01_values_and_decisions.py
python3 02_ingestion_python/00_python_foundations/02_loops_and_functions.py
python3 02_ingestion_python/00_python_foundations/03_collections_paths_libraries.py
# The final lesson deliberately exits 1 because it demonstrates a failed reconciliation.
python3 02_ingestion_python/00_python_foundations/04_mini_reconciliation.py || true
pytest -q tests                                     # no warehouse needed

# DBeaver is for learning and inspection; the setup script has already executed the
# source SQL in the correct order. Connect to localhost:5432 / meridian_core with
# username meridian and password meridian.

# 2. Snowflake platform: EITHER run 03_snowflake/01..03 in Snowsight as ACCOUNTADMIN,
#    OR `terraform apply` in 11_platform_terraform, then run the remaining applicable
#    03_snowflake scripts in numeric order (governance, search, operations, clone, DR).

# 3. First full load, then keep it streaming
cp .env.example .env   # fill in credentials
python3 02_ingestion_python/pg_to_snowflake.py            # initial load (watermark = 1900-01-01)
python3 02_ingestion_python/simulate_activity.py           # terminal 1: generates OLTP activity forever
python3 02_ingestion_python/pg_to_snowflake.py --loop 300  # terminal 2: micro-batch every 5 min

# 4. dbt (marts), then governance, then models, then scored marts
cd 04_dbt_meridian_dw && dbt deps && dbt build --target prod
#    Snowsight, ACCOUNTADMIN: 03_snowflake/06_row_level_security.sql
dbt run-operation apply_governance_all --target prod
cd .. && python3 09_decisioning_python/train_and_score.py
cd 04_dbt_meridian_dw && dbt build -s stg_ml__model_scores+ --target prod
```

Everything above is explained, with the "why", in `course/COURSE_GUIDE_TEXT.html`. The animated openings are `course/INTRO_DECK.html` and `course/WALKTHROUGHS.html`. The build checklist is `course/DRY_RUN_MAP.html`.
Offline checks are executable without credentials. Snowflake-connected SQL, dbt builds,
policies, clone recovery and the app must be run and evidenced in your own account.
