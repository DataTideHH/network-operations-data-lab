# Project Scope

## Purpose

This project connects infrastructure operations with data analysis, data quality, SQL and BI-oriented reporting.

It does not replace the separate technical labs. It provides the analytical layer above network operations and, later, virtualization operations.

## Current implemented phase

The current Cisco-oriented static sample workflow is implemented:

1. three public-safe CSV source tables
2. explicit Python header and type validation
3. reproducible SQLite database build
4. SQL analysis and data-quality views
5. aggregated public-safe report generation
6. unit tests and Python 3.12 CI
7. a documented Power BI report concept

The current model is intentionally small and explainable. It is not presented as a monitoring platform, CMDB or enterprise data warehouse.

## Relationship to other repositories

- [`cisco-switching-lab`](https://github.com/DataTideHH/cisco-switching-lab) owns the physical Cisco device, IOS maintenance, VLANs, trunks and switching validation.
- [`proxmox-virtualization-lab`](https://github.com/DataTideHH/proxmox-virtualization-lab) contains the validated pre-hardware design for a future dedicated virtualization host.
- `network-operations-data-lab` owns the sanitized source model, SQLite workflow, SQL checks, quality report and BI-oriented outputs.

The Proxmox repository exists and its pre-hardware phase is validated. A dedicated host, operational Proxmox deployment and live API source do not currently exist.

## Current source boundary

Implemented public tables:

- devices
- interfaces
- topology links

Implemented derived artifacts:

- SQLite analysis views
- aggregated data-quality report

The current source is a static synthetic baseline. It is not a historical snapshot feed.

## Future Proxmox phase

After a dedicated host has been installed and validated:

1. review actual API fields and version semantics
2. define the least-privilege extraction boundary
3. collect raw responses privately
4. sanitize identifiers before public examples are created
5. preserve source and collection timestamps separately
6. compare actual fields with the planned nodes-and-guests schema
7. extend the model only after relationships and controlled values are understood

Storage, network-assignment and backup-run tables remain deferred until live source fields have been reviewed.

## Possible future KPIs

### Current network model

- devices by role
- active and inactive interfaces
- interfaces by port role
- documentation coverage
- topology links by role and status
- data-quality pass rate
- operational warning count

### Later virtualization model

- nodes and guests by status
- allocated resources by purpose
- guests without owner or purpose
- backup-policy coverage
- backup freshness
- storage utilization
- stale collection runs

## Out of scope

- raw real infrastructure exports
- credentials, private addresses or account identifiers
- real MAC addresses or serial numbers
- full Cisco configurations
- live Proxmox claims before a host exists
- production monitoring
- enterprise-scale architecture claims
- tool inflation such as Kafka, Airflow or Kubernetes without a real requirement
