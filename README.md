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

A first Python script is included under:

```text
scripts/load_sample_data.py
```

It loads the sample CSV files, prints the records and calculates simple summaries such as interface status counts and port role counts.

This is an early data-loading step. It is intentionally simple and uses the Python standard library so the basic workflow remains easy to inspect.

## Current SQL analysis

Starter SQL analysis queries are included under:

```text
sql/sample_analysis.sql
```

The current queries demonstrate basic reporting questions such as:

- device count by role
- interface count by operational status
- access/trunk port count by port role

These queries are meant as a first bridge between networking documentation and BI-style reporting logic.

## Next steps

Planned next steps are intentionally incremental:

1. extend the sample data model with VLANs and basic topology information
2. load the sample CSV files into SQLite
3. add SQL data-quality checks
4. document a small Power BI concept based on the sample tables
5. later connect sanitized real lab outputs after the Cisco hardware baseline has been verified
