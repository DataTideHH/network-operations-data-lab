---
title: Network Operations Data Lab
description: Public-safe network operations data workflow using Python, SQLite, SQL, data-quality checks and BI-oriented reporting
---

# Network Operations Data Lab

**A reproducible portfolio project that transforms sanitized infrastructure records into a small SQLite, SQL and data-quality workflow.**

[View repository](https://github.com/DataTideHH/network-operations-data-lab) · [Read the full README](https://github.com/DataTideHH/network-operations-data-lab/blob/main/README.md) · [DataTideHH portfolio](https://datatidehh.de/)

---

## Current implemented scope

The current verified source domain is a sanitized Cisco-oriented lab baseline.

Implemented artifacts:

- `devices.csv`
- `interfaces.csv`
- `topology_links.csv`
- Python header and type validation
- reproducible SQLite database build
- SQL analysis and quality views
- aggregated public-safe report
- unit tests and Python 3.12 CI
- Power BI report concept

A dedicated Proxmox host and live API source do not currently exist. The separate Proxmox repository contains a validated pre-hardware design only.

---

## End-to-end workflow

```text
public-safe CSV source tables
            |
            v
Python contract validation
            |
            v
SQLite keys, constraints and relationships
            |
            v
SQL analysis and quality views
            |
            v
aggregated public-safe report
            |
            v
Power BI report concept
```

The workflow uses only the Python standard library.

---

## Current data model

| Table | Grain | Key |
|---|---|---|
| `devices` | one row per synthetic infrastructure device | `device_id` |
| `interfaces` | one row per interface in the current baseline | `interface_id` |
| `topology_links` | one row per directed documented relationship | `link_id` |
| `data_quality_report` | one row per executed reporting rule | check number plus name |

The current source is a static baseline rather than a historical monitoring feed.

[Read the data-model specification](data-model.md)

---

## Quality semantics

The report distinguishes:

| Category | Status | Meaning |
|---|---|---|
| `data_quality` | `OK` / `FAIL` | validity, completeness, uniqueness and relationships |
| `operational_condition` | `OK` / `WARN` | plausible operational state requiring review |
| `summary` | `INFO` | descriptive counts |

The committed sample has no data-quality failures and one intentional operational warning for an administratively enabled interface that is operationally down.

[Read the data-quality rules](data-quality-rules.md)

---

## SQLite and SQL

The implemented database layer includes:

- primary and foreign keys
- uniqueness constraints
- controlled vocabularies
- explicit Boolean and integer conversion
- non-negative speed validation
- relationship indexes
- analysis views
- aggregated check results

Source files:

- [SQLite schema](https://github.com/DataTideHH/network-operations-data-lab/blob/main/sql/schema.sql)
- [Analysis views](https://github.com/DataTideHH/network-operations-data-lab/blob/main/sql/sample_analysis.sql)
- [Quality checks](https://github.com/DataTideHH/network-operations-data-lab/blob/main/sql/data_quality_checks.sql)

SQLite binaries remain local and are not committed.

---

## Reproduce locally

```bash
python -m scripts.load_sample_data
python -m scripts.build_sqlite_database
python -m scripts.run_sqlite_analysis
python -m scripts.run_data_quality_checks
python -m unittest discover -s tests -p "test_*.py" -v
```

The committed report is regenerated in CI and compared with the repository version.

---

## Portfolio evidence

| Artifact | Evidence |
|---|---|
| [Project scope](project-scope.md) | boundaries and current implementation status |
| [Data model](data-model.md) | grain, keys, relationships and controlled values |
| [Data-quality rules](data-quality-rules.md) | hard validation and reporting semantics |
| [Cisco baseline](cisco-switch-baseline.md) | source context without private raw output |
| [Lab topology](lab-topology.md) | current data path and future cross-layer design |
| [VLAN roadmap](vlan-lab-roadmap.md) | aligned VLAN 10/20/30/99/998/999 roles |
| [Proxmox roadmap](proxmox-data-integration-roadmap.md) | future source integration without live claims |
| [Power BI concept](https://github.com/DataTideHH/network-operations-data-lab/blob/main/powerbi/report-concept.md) | report questions, pages, measures and limitations |
| [Quality report](https://github.com/DataTideHH/network-operations-data-lab/blob/main/data/processed/data_quality_report.csv) | reproducible aggregated output |
| [Tests](https://github.com/DataTideHH/network-operations-data-lab/blob/main/tests/test_network_operations_workflow.py) | executable workflow verification |

---

## Public-safety boundary

The repository does not publish real:

- IP or MAC addresses
- serial numbers
- hostnames
- account identifiers
- configurations
- tokens or fingerprints
- private topology
- raw infrastructure responses

Only synthetic and aggregated public-safe records are committed.

---

## Power BI status

No `.pbix` or `.pbit` file is published.

The current artifact is a reviewed report concept covering:

1. Infrastructure Overview
2. Interface Operations
3. Topology Coverage
4. Data Quality

A screenshot should be published only after a local model is stable and privacy-reviewed.

---

## Related projects

- [Cisco Switching Lab](https://datatidehh.github.io/cisco-switching-lab/) — physical Cisco device, IOS maintenance and switching labs
- [Proxmox Virtualization Lab](https://datatidehh.github.io/proxmox-virtualization-lab/) — validated pre-hardware virtualization design
- [Music Production Data Lab](https://datatidehh.github.io/music-production-data-lab/) — a separate structured Data/BI domain
- [IPv4 Subnet Calculator Multilang](https://datatidehh.github.io/ipv4-subnet-calculator-multilang/) — tested IPv4/CIDR logic in three languages

---

## Next substantive milestone

The Cisco-based static workflow is complete for its current scope.

The next useful portfolio step is a small local Power BI prototype based on the SQLite model. Proxmox integration begins only after dedicated hardware exists and private source fields have been reviewed.
