# Network Operations Data Lab

Network Operations Data Lab is a learning and portfolio project that connects networking fundamentals with a Data/BI workflow.

The goal is not only to configure network devices, but to treat network operations as a structured data source.

## Project idea

This lab explores how operational network data can be collected, cleaned, modeled, queried and visualized.

Planned data sources include:

- device inventory
- interface status
- VLAN documentation
- trunk/access port information
- error counters
- configuration snapshots
- basic availability checks
- lab topology documentation

## Planned stack

- Cisco switching and routing lab
- Python for parsing and data preparation
- CSV and SQLite for structured storage
- SQL for analysis and validation
- Power BI for reporting and dashboard prototypes
- Markdown documentation for reproducibility

## Current focus

This project is currently in an early learning-lab stage.

The first phase is aligned with CCNA-level networking fundamentals:

- switching basics
- VLANs
- trunk ports
- STP basics
- interface documentation
- subnetting and Layer 3 concepts
- network troubleshooting notes

## Data and privacy

This repository is designed to be public-safe.

Real device identifiers, MAC addresses, public IP addresses, Tailscale IPs, serial numbers, hostnames and private network details must not be published here.

All examples should use anonymized or sample data.

## Why this project matters

For Data/BI work, operational IT systems are important data sources.

This project demonstrates how infrastructure data can be transformed into useful reporting structures, combining:

- networking fundamentals
- data preparation
- SQL-based analysis
- BI-style visualization
- technical documentation

## Repository structure

    network-operations-data-lab/
    ├── data/
    │   ├── sample/
    │   └── processed/
    ├── docs/
    ├── powerbi/
    ├── scripts/
    ├── sql/
    ├── .gitignore
    └── README.md

## Status

Early lab / in progress.

This repository is connected to my Data/BI Analyst track and my CCNA preparation.

---

## Current included sample data

The repository currently includes small public-safe CSV sample files under:

```text
data/sample/
```

Current sample files:

| File | Purpose |
|---|---|
| `devices.csv` | Small anonymized device inventory with sample switches and a lab router |
| `interfaces.csv` | Small anonymized interface dataset with admin status, operational status, VLAN and port role fields |

The sample data is intentionally synthetic/anonymized and does not contain real serial numbers, MAC addresses, public IP addresses, private IP addresses or sensitive hostnames.

## Current scripts

Python helper scripts are included under:

- `scripts/load_sample_data.py`
- `scripts/run_data_quality_checks.py`

`load_sample_data.py` loads the public-safe sample CSV files, prints the records and calculates simple summaries such as interface status counts and port role counts.

`run_data_quality_checks.py` runs a numbered, public-safe data-quality check workflow aligned with `sql/data_quality_checks.sql`. It uses only the Python standard library and writes an aggregated report to `data/processed/data_quality_report.csv`.

The generated report contains only check numbers, check names, categories, statuses, affected row counts and short descriptions. It does not write device names, interface names or row-level identifiers.

## Current SQL analysis

Starter SQL analysis and validation queries are included under:

- `sql/sample_analysis.sql`
- `sql/data_quality_checks.sql`

The current SQL files demonstrate basic reporting and data-quality questions such as:

- device count by role
- interface count by operational status
- access/trunk port count by port role
- missing device or interface identifiers
- duplicate device or interface records
- interfaces referencing unknown devices
- interfaces administratively up but operationally down

These queries are meant as a first bridge between networking documentation, data-quality checks and BI-style reporting logic.

## Current data-quality report

A public-safe data-quality report is generated under:

- `data/processed/data_quality_report.csv`

The report is intentionally aggregated. It shows the check number, check name, category, status, affected row count and a short description, but it does not expose device names, interface names or other row-level identifiers.

The current sample report contains one expected finding for check 11, because the synthetic sample data includes an administratively up but operationally down interface. This demonstrates that the validation workflow can detect operational data-quality issues without exposing sensitive details.

## Next steps

Planned next steps are intentionally incremental:

1. load the sample CSV files into SQLite
2. extend the sample data model with VLANs and basic topology information
3. document a small Power BI concept based on the sample tables
4. maintain a public-safe Cisco switch baseline document
5. plan VLAN 10 / VLAN 20 / VLAN 30 as an incremental CCNA lab roadmap
6. later connect sanitized real lab outputs after the Cisco hardware baseline has been verified
