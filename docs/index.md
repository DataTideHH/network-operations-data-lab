---
title: Network Operations Data Lab
description: Public-safe network operations data, SQL and BI portfolio project
---

# Network Operations Data Lab

**A public-safe portfolio project that treats network operations as a structured data source for Python, SQL, data-quality checks and BI-style reporting.**

[View repository](https://github.com/DataTideHH/network-operations-data-lab) · [Read the full README](https://github.com/DataTideHH/network-operations-data-lab/blob/main/README.md)

---

## Project purpose

Network operations data is often scattered across device inventories, interface status outputs, VLAN notes, configuration snapshots and troubleshooting records.

This project turns that idea into a small, reproducible Data/BI workflow:

- document a sanitized Cisco switching lab baseline
- model public-safe device and interface data
- load sample data with Python
- run SQL-style data-quality checks
- generate an aggregated public-safe quality report
- prepare the structure for later SQLite and Power BI reporting

The goal is not only to configure network devices. The goal is to show how operational IT systems can become reliable reporting data sources.

---

## Why this matters for Data/BI

For process analysis and BI work, infrastructure and service operations are practical data domains.

This project connects several skills in one place:

| Area | Portfolio signal |
|---|---|
| Networking | CCNA-oriented switching concepts, VLANs, trunks, interface status and lab documentation |
| Data modeling | Device inventory, interface records, port roles, operational status and public-safe identifiers |
| Data quality | Checks for missing identifiers, duplicates, unknown references and operational inconsistencies |
| Python | Sample data loading and reproducible report generation |
| SQL / BI | Starter analysis queries and BI-style summary logic |
| Documentation | Public/private separation and explainable technical workflow |

---

## Current workflow

```text
Cisco lab baseline
-> sanitized sample inventory and interface data
-> Python loading and validation scripts
-> SQL analysis and data-quality checks
-> aggregated public-safe report
-> future SQLite and Power BI reporting layer
```

---

## Current portfolio artifacts

| Artifact | What it shows |
|---|---|
| [Project scope](project-scope.md) | How the project connects network operations, data analysis and BI reporting |
| [Cisco switch baseline](cisco-switch-baseline.md) | Public-safe description of the verified local switching baseline |
| [Lab topology](lab-topology.md) | Sanitized topology concept without private network details |
| [VLAN lab roadmap](vlan-lab-roadmap.md) | Incremental VLAN learning plan with safe lab-only phases |
| [Data-quality rules](data-quality-rules.md) | Validation checks for network operations sample data |
| [Sample devices CSV](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/sample/devices.csv) | Public-safe device inventory sample |
| [Sample interfaces CSV](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/sample/interfaces.csv) | Public-safe interface status and port-role sample |
| [Data-quality report](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/processed/data_quality_report.csv) | Aggregated quality-check output without row-level identifiers |
| [SQL checks](https://github.com/DataTideHH/network-operations-data-lab/blob/main/sql/data_quality_checks.sql) | SQL validation logic for the sample model |
| [Python checks](https://github.com/DataTideHH/network-operations-data-lab/blob/main/scripts/run_data_quality_checks.py) | Reproducible data-quality report generation |

---

## Public-safe data model

The current model uses small anonymized sample tables.

| Table | Role |
|---|---|
| `devices.csv` | Device inventory with roles and public-safe identifiers |
| `interfaces.csv` | Interface records with status, VLAN and port role fields |
| `data_quality_report.csv` | Aggregated validation output for reporting and review |

The sample data intentionally excludes real serial numbers, MAC addresses, public IP addresses, private IP addresses, hostnames and full configuration exports.

---

## Current data-quality focus

The current checks demonstrate practical operational reporting questions, including:

- missing device or interface identifiers
- duplicate inventory or interface records
- interfaces referencing unknown devices
- admin-up interfaces that are operationally down
- basic summaries by device role, port role and operational status

This is deliberately small, but it mirrors a real Data/BI pattern: operational records need validation before they become trusted reporting data.

---

## What this demonstrates

- network operations as a data source
- sanitized public portfolio documentation
- public/private data separation
- Python-based CSV processing
- SQL-style validation and analysis
- data-quality thinking in an IT operations context
- a bridge between CCNA fundamentals and Data/BI reporting
- preparation for Power BI dashboards and service operations KPIs

---

## Next steps

The next useful project steps are:

1. load the sample CSV files into SQLite
2. extend the sample model with sanitized topology and port-description fields
3. add sanitized interface snapshot examples
4. document a small Power BI reporting concept
5. publish reviewed dashboard screenshots once the model is stable
