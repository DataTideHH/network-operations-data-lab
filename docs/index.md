---
title: Network Operations Data Lab
description: Public-safe infrastructure operations data, SQL and BI portfolio project
---

# Network Operations Data Lab

**A public-safe portfolio project that treats infrastructure operations as structured data sources for Python, SQL, data-quality checks and BI-style reporting.**

[View repository](https://github.com/DataTideHH/network-operations-data-lab) · [Read the full README](https://github.com/DataTideHH/network-operations-data-lab/blob/main/README.md) · [DataTideHH portfolio](https://datatidehh.de/)

---

## Project purpose

Operational data is often scattered across device inventories, interface status outputs, VLAN notes, configuration snapshots, virtualization inventories, backup records and troubleshooting logs.

This project turns that idea into a small, reproducible Data/BI workflow:

- document a sanitized Cisco switching lab baseline
- model public-safe device and interface data
- load sample data with Python
- run SQL-style data-quality checks
- generate an aggregated public-safe quality report
- prepare the structure for later SQLite and Power BI reporting
- define a future Proxmox data-source roadmap without claiming an existing deployment

The current verified source domain is the Cisco lab. Proxmox remains a planned later source after dedicated x86 hardware is available and the separate virtualization lab has been installed and validated.

The goal is not only to configure infrastructure. The goal is to show how operational IT systems can become reliable reporting data sources.

---

## Why this matters for Data/BI

For process analysis and BI work, infrastructure and service operations are practical data domains.

This project connects several skills in one place:

| Area | Portfolio signal |
|---|---|
| Networking | CCNA-oriented switching concepts, VLANs, trunks, interface status and lab documentation |
| Virtualization roadmap | Future Proxmox nodes, guests, storage, networks and backup metadata |
| Data modeling | Inventory, operational status, ownership, relationships and public-safe identifiers |
| Data quality | Completeness, duplicates, unknown references, freshness and operational inconsistencies |
| Python | Sample data loading, future API extraction and reproducible report generation |
| SQL / BI | Starter analysis queries, validation logic and BI-style summaries |
| Documentation | Public/private separation, explicit implementation status and explainable workflow |

---

## Current and future workflow

```text
Current Cisco lab baseline
-> sanitized sample inventory and interface data
-> Python loading and validation scripts
-> SQL analysis and data-quality checks
-> aggregated public-safe report
-> future SQLite and Power BI reporting layer

Future dedicated Proxmox lab
-> least-privilege REST API extraction
-> private raw collection and public-safe sanitization
-> node, guest, storage, network and backup tables
-> cross-layer quality checks and operational reporting
```

---

## Current portfolio artifacts

| Artifact | What it shows |
|---|---|
| [Project scope](project-scope.md) | How the project separates technical labs from the Data/BI layer |
| [Cisco switch baseline](cisco-switch-baseline.md) | Public-safe description of the verified local switching baseline |
| [Lab topology](lab-topology.md) | Current Cisco topology and future cross-layer architecture |
| [VLAN lab roadmap](vlan-lab-roadmap.md) | Incremental VLAN learning plan with safe lab-only phases |
| [Proxmox data integration roadmap](proxmox-data-integration-roadmap.md) | Planned source entities, checks, KPIs and implementation phases |
| [Data-quality rules](data-quality-rules.md) | Validation checks for network operations sample data |
| [Sample devices CSV](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/sample/devices.csv) | Public-safe device inventory sample |
| [Sample interfaces CSV](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/sample/interfaces.csv) | Public-safe interface status and port-role sample |
| [Data-quality report](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/processed/data_quality_report.csv) | Aggregated quality-check output without row-level identifiers |
| [SQL checks](https://github.com/DataTideHH/network-operations-data-lab/blob/main/sql/data_quality_checks.sql) | SQL validation logic for the current sample model |
| [Python checks](https://github.com/DataTideHH/network-operations-data-lab/blob/main/scripts/run_data_quality_checks.py) | Reproducible data-quality report generation |

---

## Public-safe data model

The current model uses small anonymized network sample tables.

| Table | Role |
|---|---|
| `devices.csv` | Device inventory with roles and public-safe identifiers |
| `interfaces.csv` | Interface records with status, VLAN and port role fields |
| `data_quality_report.csv` | Aggregated validation output for reporting and review |

Future synthetic Proxmox examples may add:

- `proxmox_nodes.csv`
- `proxmox_guests.csv`
- `proxmox_storage.csv`
- `proxmox_network_assignments.csv`
- `proxmox_backups.csv`

These files should only be added after the schema has been reviewed. They must not contain real node names, VM IDs, addresses, API tokens, fingerprints or private topology.

---

## Current data-quality focus

The current checks demonstrate practical operational reporting questions, including:

- missing device or interface identifiers
- duplicate inventory or interface records
- interfaces referencing unknown devices
- admin-up interfaces that are operationally down
- basic summaries by device role, port role and operational status

The future Proxmox model extends this pattern toward ownership, backup coverage, resource allocations, storage utilization, collection freshness and cross-table relationships.

This is deliberately small, but it mirrors a real Data/BI pattern: operational records need validation before they become trusted reporting data.

---

## What this demonstrates

- infrastructure operations as data sources
- sanitized public portfolio documentation
- public/private data separation
- explicit distinction between current implementation and roadmap
- Python-based CSV processing and future API collection
- SQL-style validation and analysis
- data-quality thinking in an IT operations context
- a bridge between CCNA fundamentals, virtualization and Data/BI reporting
- preparation for Power BI dashboards and service operations KPIs

---

## Related DataTideHH project pages

- [Cisco Switching Lab](https://datatidehh.github.io/cisco-switching-lab/) — physical switching, management, VLAN and troubleshooting lab
- [Music Production Data Lab](https://datatidehh.github.io/music-production-data-lab/) — public-safe data modeling, SQL/Python workflow and Power BI reporting layer
- [Spring Boot Process API Basics](https://datatidehh.github.io/spring-boot-process-api-basics/) — small Java/Spring REST API for structured process-check data

---

## Next steps

The next useful project steps are:

1. load the current sample CSV files into SQLite
2. extend the network model with sanitized topology and port-description fields
3. add sanitized interface snapshot examples
4. review the proposed Proxmox entities and controlled vocabularies
5. create synthetic Proxmox sample tables without claiming live collection
6. document a small Power BI reporting concept
7. publish reviewed dashboard screenshots once the model is stable
8. begin live private API collection only after dedicated hardware exists