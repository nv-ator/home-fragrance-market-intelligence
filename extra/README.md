# Extra / Auxiliary Artifacts

This folder contains development-only, exploratory, historical, and auxiliary artifacts retained for reference but not required for the final application.

## Contents

- **`reports/`**: Intermediate and QA stage reports (`DATA_COLLECTION_REPORT.md`, `DATA_QUALITY_REPORT.md`, `DATABASE_QUALITY_REPORT.md`, `DASHBOARD_QA_REPORT.md`, `PIPELINE_RUN_REPORT.md`). Authoritative metrics and submission documentation reside in `docs/` and root `README.md`.
- **`scripts/`**: Auxiliary, exploratory, and verification scripts used during development (`compute_authoritative_metrics.py`, `inspect_api_endpoints.py`, `print_coverage_table.py`, `validate_api_responses.py`). The production pipeline is executed via the root `main.py`.
