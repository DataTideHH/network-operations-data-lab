# Network Operations Data Lab

Network Operations Data Lab is a learning and portfolio project that connects networking and infrastructure operations with a Data/BI workflow.

Project page: https://datatidehh.github.io/network-operations-data-lab/

The goal is not only to configure infrastructure, but to treat operational systems as structured data sources.

The current verified source domain is the Cisco switching lab. A future Proxmox virtualization lab is included in the data architecture roadmap, but no operational Proxmox host or real Proxmox API export is currently claimed.

## Project idea

This lab explores how operational infrastructure data can be collected, cleaned, modeled, queried and visualized.

Current and planned data sources include:

- network device inventory
- interface status
- VLAN documentation
- trunk/access port information
- error counters
- configuration snapshots
- basic availability checks
- lab topology documentation
- future Proxmox node and guest inventory
- future virtual network and storage inventory
- future backup-status and resource-allocation records

## Current and planned stack

- Cisco switching and routing lab
- future Proxmox virtualization lab and REST API
- Python for parsing, API access and data preparation
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

The Data/BI side focuses on turning operational records into structured, validated and reportable sample data.

Proxmox-related files currently document only the future data model and integration path. Real API collection should begin only after a dedicated x86 host has been installed, secured and validated in the separate [`proxmox-virtualization-lab`](https://github.com/DataTideHH/proxmox-virtualization-lab) repository.

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

Real device identifiers, MAC addresses, public IP addresses, Tailscale IPs, serial numbers, hostnames, Proxmox node names, VM names, API tokens, cluster fingerprints and private network details must not be published here.

All examples should use anonymized or synthetic data.

## Why this project matters

For Data/BI work, operational IT systems are important data sources.

This project demonstrates how infrastructure data can be transformed into useful reporting structures, combining:

- networking and virtualization fundamentals
- data preparation
- SQL-based analysis
- data-quality rules
- BI-style visualization
- technical documentation

The longer-term portfolio story is intentionally cross-layer:

```text
Cisco physical network
        |
        v
future Proxmox virtualization platform
        |
        v
REST API / sanitized exports
        |
        v
Python + SQLite + SQL data-quality workflow
        |
        v
Power BI operational reporting
```

## Repository structure

```text
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
│   ├── proxmox-data-integration-roadmap.md
│   └── vlan-lab-roadmap.md
├── powerbi/
├── scripts/
├── sql/
├── .gitignore
└── README.md
```

## Status

Active learning-lab / in progress.

The repository already contains public-safe Cisco sample data, Python processing scripts, SQL analysis and validation files, an aggregated data-quality report and a GitHub Pages project landing page.

It is connected to my Data/BI Analyst track and my CCNA preparation by treating infrastructure operations as a structured reporting domain. Proxmox is currently represented only as a carefully separated future data-source roadmap.

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

Future Proxmox sample tables should remain separate from the current Cisco baseline until their schemas and source semantics are documented.

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

Future Proxmox checks may cover undocumented guests, missing ownership, stale backups, resource-allocation anomalies and invalid relationships between nodes, guests, storage and networks.

## Current data-quality report

A public-safe data-quality report is generated under:

- `data/processed/data_quality_report.csv`

The report is intentionally aggregated. It shows the check number, check name, category, status, affected row count and a short description, but it does not expose device names, interface names or other row-level identifiers.

The current sample report contains one expected finding for check 11, because the synthetic sample data includes an administratively up but operationally down interface. This demonstrates that the validation workflow can detect operational data-quality issues without exposing sensitive details.

## GitHub Pages project site

This repository includes a small project landing page under:

```text
docs/index.md
```

After GitHub Pages is enabled for the repository, the published site is available at:

```text
https://datatidehh.github.io/network-operations-data-lab/
```

Recommended GitHub Pages settings:

```text
Source: Deploy from a branch
Branch: main
Folder: /docs
```

## Next steps

Planned next steps are intentionally incremental:

1. load the current sample CSV files into SQLite
2. extend the current network sample model with sanitized topology and port-description fields
3. add sanitized sample snapshots for interface description, interface status and MAC-table summaries
4. document the future Proxmox source entities and public-safe sample schemas
5. create synthetic `proxmox_nodes`, `proxmox_guests`, `proxmox_storage` and `proxmox_backups` datasets only after the model is reviewed
6. build initial cross-source data-quality rules without claiming live API collection
7. document a small Power BI concept based on the sample tables
8. after dedicated hardware exists, replace selected synthetic assumptions with sanitized API-derived examples
9. keep real topology, configurations, addresses, tokens, identifiers and account data out of the public repository