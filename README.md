# Network Operations Data Lab

[![GitHub Pages](https://github.com/DataTideHH/network-operations-data-lab/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/DataTideHH/network-operations-data-lab/actions/workflows/pages/pages-build-deployment)

Network Operations Data Lab is a public-safe learning and portfolio project that turns sanitized infrastructure records into a reproducible Data/BI workflow.

Project page: https://datatidehh.github.io/network-operations-data-lab/

## Current verified scope

The current implemented source domain is a sanitized Cisco-oriented lab baseline. The repository contains:

- three related CSV source tables
- a Python standard-library loader and workflow layer
- a normalized SQLite database build
- SQL analysis views and SQL-defined validation rules
- an aggregated public-safe quality report
- unit tests and Python 3.12 CI
- a Power BI report concept
- a separate, clearly labelled Proxmox integration roadmap

A dedicated Proxmox host, operational Proxmox deployment and live API extraction do not currently exist. The separate [`proxmox-virtualization-lab`](https://github.com/DataTideHH/proxmox-virtualization-lab) repository contains the validated pre-hardware design.

## Why this project exists

Operational IT systems produce inventories, status records, relationships and exceptions that can be treated as structured analytical data.

The current workflow demonstrates:

```text
sanitized Cisco-oriented CSV samples
                |
                v
Python header and type validation
                |
                v
SQLite tables, keys and constraints
                |
                v
SQL analysis and validation views
                |
                v
aggregated public-safe quality report
                |
                v
Power BI reporting concept
```

This repository owns the data layer. Physical Cisco configuration belongs in [`cisco-switching-lab`](https://github.com/DataTideHH/cisco-switching-lab). Hypervisor administration belongs in [`proxmox-virtualization-lab`](https://github.com/DataTideHH/proxmox-virtualization-lab).

## Current source tables

| File | Grain | Primary key |
|---|---|---|
| `data/sample/devices.csv` | one row per synthetic infrastructure device | `device_id` |
| `data/sample/interfaces.csv` | one row per interface in the current sample baseline | `interface_id` |
| `data/sample/topology_links.csv` | one row per directed documented relationship | `link_id` |

The current sample is a static baseline, not a historical time series. It contains five devices, five interfaces and three topology links.

Detailed grain, keys, relationships and controlled vocabularies are documented in [`docs/data-model.md`](docs/data-model.md).

## Public-safety boundary

Never publish:

- real IP or MAC addresses
- serial numbers
- real hostnames or account identifiers
- full running configurations
- API tokens, ticket cookies or fingerprints
- private topology or raw infrastructure exports
- backup credentials or private VM identifiers

The committed CSV files and report use synthetic identifiers and aggregated findings only.

## Reproducible workflow

All current Python code uses only the Python standard library.

### Inspect the CSV samples

```bash
python -m scripts.load_sample_data
```

### Build the SQLite database

```bash
python -m scripts.build_sqlite_database
```

This creates the ignored local file:

```text
data/processed/network_operations.db
```

The build:

1. verifies exact ordered CSV headers
2. converts Boolean and integer fields explicitly
3. creates the SQLite schema
4. loads devices, interfaces and topology links in dependency order
5. installs SQL analysis and quality views
6. runs `PRAGMA foreign_key_check`

### Run the SQLite analysis views

```bash
python -m scripts.run_sqlite_analysis
```

The current views cover:

- device counts by role
- interface status combinations
- interface counts by port role
- topology links by role and status
- interface-description coverage

### Generate the public-safe quality report

```bash
python -m scripts.run_data_quality_checks
```

Output:

```text
data/processed/data_quality_report.csv
```

The report contains only:

- check number
- check name
- category
- status
- affected-row count
- short description

It does not publish row-level infrastructure identifiers.

## Quality semantics

The report deliberately separates three meanings:

| Category | Status behavior | Meaning |
|---|---|---|
| `data_quality` | `OK` or `FAIL` | completeness, validity, uniqueness and relationship quality |
| `operational_condition` | `OK` or `WARN` | a plausible operational state that may require review |
| `summary` | `INFO` | descriptive counts, not pass/fail rules |

The committed sample has no `data_quality` failures. It intentionally contains one `operational_condition` warning: one administratively enabled interface is operationally down. This demonstrates an operations exception without misclassifying correct source data as bad data.

## SQLite model

The schema under [`sql/schema.sql`](sql/schema.sql) provides:

- primary keys for all three source entities
- foreign keys from interfaces to devices
- composite source-interface validation for topology links
- target-device validation
- unique device/interface and topology relationships
- controlled values through `CHECK` constraints
- non-negative interface speed
- Boolean storage as `0` and `1`
- indexes for common relationship and status queries

SQLite database binaries are local build artifacts and are not committed.

## SQL layer

| File | Purpose |
|---|---|
| [`sql/schema.sql`](sql/schema.sql) | tables, keys, constraints and indexes |
| [`sql/sample_analysis.sql`](sql/sample_analysis.sql) | reusable BI-oriented analysis views |
| [`sql/data_quality_checks.sql`](sql/data_quality_checks.sql) | aggregated quality, operations and summary results |

Python orchestrates loading and report export; SQL contains the analytical and validation logic executed against the current three-table model.

## Tests and CI

Run locally:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The tests verify:

- the three committed CSV contracts and row counts
- Boolean and integer conversion
- SQLite build and foreign-key integrity
- analysis-view availability
- separation of data failures and operational warnings
- deterministic report generation
- rejection of invalid Boolean and relationship data
- detection of device-ID/name inconsistencies
- dependency-free CLI execution

GitHub Actions uses Python 3.12 to compile the code, run tests, build SQLite, run analysis, regenerate the report and verify that the committed report remains current.

## Power BI status

No `.pbix` file is committed. The current public artifact is [`powerbi/report-concept.md`](powerbi/report-concept.md), which defines:

- intended audience
- report questions
- table relationships
- candidate measures
- proposed report pages
- the distinction between data quality and operational warnings
- limitations of the current static sample

A reviewed screenshot or public template should be added only after a local Power BI prototype is stable and contains no private data.

## Proxmox roadmap

The separate Proxmox repository now contains a validated pre-hardware design and a synthetic schema `0.1` covering nodes and guests. This repository does not yet ingest those records.

Storage, network-assignment and backup-run entities remain roadmap items until real API fields and source semantics have been reviewed on a dedicated lab host. No live Proxmox collection is claimed.

See [`docs/proxmox-data-integration-roadmap.md`](docs/proxmox-data-integration-roadmap.md).

## VLAN alignment

The connected lab repositories use the same planned VLAN roles:

| VLAN | Role |
|---:|---|
| 10 | test clients |
| 20 | lab systems |
| 30 | test services and servers |
| 99 | management |
| 998 | unused native VLAN for lab trunks |
| 999 | parking VLAN for shut unused access ports |

VLAN 998 has no SVI or attached endpoint. VLAN 999 is not used as a trunk native VLAN.

## Repository structure

```text
network-operations-data-lab/
├── .github/workflows/ci.yml
├── data/
│   ├── sample/
│   │   ├── devices.csv
│   │   ├── interfaces.csv
│   │   └── topology_links.csv
│   └── processed/
│       └── data_quality_report.csv
├── docs/
│   ├── index.md
│   ├── project-scope.md
│   ├── data-model.md
│   ├── data-quality-rules.md
│   ├── cisco-switch-baseline.md
│   ├── lab-topology.md
│   ├── vlan-lab-roadmap.md
│   └── proxmox-data-integration-roadmap.md
├── powerbi/
│   ├── README.md
│   └── report-concept.md
├── scripts/
│   ├── workflow.py
│   ├── load_sample_data.py
│   ├── build_sqlite_database.py
│   ├── run_sqlite_analysis.py
│   └── run_data_quality_checks.py
├── sql/
│   ├── schema.sql
│   ├── sample_analysis.sql
│   └── data_quality_checks.sql
└── tests/
    └── test_network_operations_workflow.py
```

## Current status and next milestone

The Cisco-based static sample workflow is implemented and reproducible.

The next substantive portfolio milestone should be a small local Power BI prototype based on the SQLite model. A later Proxmox phase should begin only after dedicated hardware exists and private API fields have been reviewed.
