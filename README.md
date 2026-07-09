# Network Operations Data Lab

Network Operations Data Lab is a learning and portfolio project that connects networking fundamentals with a Data/BI workflow.

Project page: https://datatidehh.github.io/network-operations-data-lab/

The goal is not only to configure network devices, but to treat network operations as a structured data source.

## Project idea

This lab explores how operational network data can be collected, cleaned, modeled, queried and visualized.

Relevant data sources include:

- device inventory
- interface status
- VLAN documentation
- trunk/access port information
- error counters
- configuration snapshots
- basic availability checks
- lab topology documentation

## Current and planned stack

- Cisco switching and routing lab
- Python for parsing and data preparation
- CSV and SQLite for structured storage
- SQL for analysis and validation
- Power BI for reporting and dashboard prototypes
- Markdown documentation for reproducibility

## Current focus

This project is an active learning-lab and portfolio project. The current public version already includes a sanitized Cisco lab baseline, public-safe sample data, Python helper scripts, SQL analysis files and an aggregated data-quality report.

The networking foundation remains aligned with CCNA-level topics:

- switching basics
- VLANs
- trunk ports
- STP basics
- interface documentation
- subnetting and Layer 3 concepts
- network troubleshooting notes

The Data/BI side focuses on turning those operational records into structured, validated and reportable sample data.

## Current verified lab baseline

A small Cisco switching baseline has been verified in a local private lab environment. The public repository does not publish the real home-network topology, but the sanitized baseline now includes:

- console access from macOS through a USB-serial workflow
- SSH access for normal local administration
- a management SVI receiving a stable DHCP-reserved address from the local router
- one uplink path through a local wireless bridge/repeater
- two client-facing access links negotiating at 1 Gbit/s full duplex
- public-safe interface descriptions for the active lab ports
- successful local gateway and external reachability checks

Real IP addresses, MAC addresses, serial numbers, hostnames and private network details are intentionally excluded.

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
    │   ├── _config.yml
    │   ├── index.md
    │   ├── cisco-switch-baseline.md
    │   ├── data-quality-rules.md
    │   ├── lab-topology.md
    │   ├── project-scope.md
    │   └── vlan-lab-roadmap.md
    ├── powerbi/
    ├── scripts/
    ├── sql/
    ├── .gitignore
    └── README.md

## Status

Active learning-lab / in progress.

The repository already contains public-safe sample data, Python processing scripts, SQL analysis and validation files, an aggregated data-quality report and a GitHub Pages project landing page.

It is connected to my Data/BI Analyst track and my CCNA preparation by treating network operations as a structured reporting domain.

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

## GitHub Pages project site

This repository includes a small project landing page under:

    docs/index.md

After GitHub Pages is enabled for the repository, the published site is available at:

    https://datatidehh.github.io/network-operations-data-lab/

Recommended GitHub Pages settings:

    Source: Deploy from a branch
    Branch: main
    Folder: /docs

## Next steps

Planned next steps are intentionally incremental:

1. load the sample CSV files into SQLite
2. extend the sample data model with sanitized topology and port-description fields
3. add sanitized sample snapshots for interface description, interface status and MAC-table summaries
4. document a small Power BI concept based on the sample tables
5. continue the VLAN 10 / VLAN 20 / VLAN 30 roadmap only on lab-only ports
6. keep real topology, configuration exports, IP addresses, MAC addresses and device identifiers out of the public repository
