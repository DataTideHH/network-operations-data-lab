# Proxmox Data Integration Roadmap

## Status

This document defines a future data source and does not represent an operational Proxmox environment. A dedicated x86 host has not yet been acquired.

## Objective

The future Proxmox integration should demonstrate how virtualization operations data can be collected, modelled, validated and reported without exposing private infrastructure details.

The technical installation and administration of the hypervisor will belong in `proxmox-virtualization-lab`. This repository will receive only sanitized operational metadata and will focus on the Data/BI workflow.

## Source domains

The first useful source entities are intentionally small:

| Entity | Example analytical purpose |
|---|---|
| nodes | host inventory, status and resource capacity |
| guests | VM and LXC inventory, lifecycle status and ownership |
| storage | capacity, utilization and availability |
| networks | bridge and VLAN assignment coverage |
| backups | policy coverage, status and freshness |
| snapshots | lifecycle and retention review |
| collection runs | extraction timestamp, status and row counts |

## Proposed public-safe sample tables

### `proxmox_nodes`

- `node_key`
- `node_status`
- `cpu_threads`
- `memory_total_mb`
- `storage_total_gb`
- `environment`
- `source_timestamp_utc`
- `collected_at_utc`

### `proxmox_guests`

- `guest_key`
- `node_key`
- `guest_type`
- `guest_status`
- `purpose_category`
- `owner_role`
- `cpu_allocated`
- `memory_allocated_mb`
- `backup_policy_key`
- `environment`
- `source_timestamp_utc`
- `collected_at_utc`

### `proxmox_storage`

- `storage_key`
- `node_key`
- `storage_type`
- `content_types`
- `capacity_total_gb`
- `capacity_used_gb`
- `storage_status`
- `collected_at_utc`

### `proxmox_network_assignments`

- `assignment_key`
- `guest_key`
- `bridge_key`
- `vlan_key`
- `interface_role`
- `collected_at_utc`

### `proxmox_backups`

- `backup_event_key`
- `guest_key`
- `backup_policy_key`
- `backup_status`
- `started_at_utc`
- `finished_at_utc`
- `age_hours_at_collection`
- `collected_at_utc`

The keys above should be synthetic public identifiers, not real node names, VM IDs or storage IDs.

## Initial data-quality rules

### Completeness

- every guest has a guest type and lifecycle status
- every running guest has a documented purpose category
- every non-temporary guest has an owner role
- every protected guest has a backup policy

### Referential integrity

- every guest references a known node
- every storage record references a known node
- every network assignment references a known guest
- every backup event references a known guest and policy

### Validity

- CPU and memory allocations are non-negative
- used storage does not exceed total storage
- allowed guest types are limited to reviewed values such as `qemu` and `lxc`
- lifecycle and backup status values use controlled vocabularies

### Freshness

- collection timestamps are present
- source timestamps are not later than collection timestamps
- the newest backup remains within its documented policy threshold
- inventory extracts are not older than the reporting service-level target

### Policy and documentation

- production-like labels are not used for temporary learning guests
- management network assignments follow the documented design
- stopped or archived guests have an explicit retention decision
- snapshots older than the agreed threshold are flagged for review

## Candidate KPIs

- running, stopped and template guests
- VM versus LXC distribution
- allocated CPU and memory by purpose category
- host resource allocation ratio
- storage utilization by node and storage type
- backup success rate
- guests without current backup
- guests without documented owner or purpose
- stale inventory collections
- management, server and lab network assignment coverage

## Extraction principles

When hardware exists, the first extraction should follow these rules:

1. use a dedicated least-privilege API token
2. request only fields required for the defined model
3. never commit tokens, ticket cookies or raw private responses
4. separate collection from sanitization
5. retain collection logs without sensitive payloads
6. keep raw private extracts outside the public repository
7. publish only synthetic or reviewed anonymized examples
8. distinguish source time from collection time
9. document API assumptions and version dependencies

## Incremental implementation plan

### Phase 0: schema-only roadmap

- review entity and field definitions
- create synthetic CSV examples
- define controlled vocabularies
- write SQL DDL and initial checks

### Phase 1: local synthetic workflow

- load sample tables into SQLite
- implement Python validation
- generate an aggregated quality report
- draft a Power BI semantic model

### Phase 2: first live private extraction

- install and secure the separate Proxmox lab
- create a least-privilege token
- perform a private local API export
- compare actual fields with the planned schema
- revise the model before publishing examples

### Phase 3: sanitized portfolio integration

- map real source semantics to synthetic public identifiers
- publish reviewed sample extracts
- document extraction, transformation and validation
- add selected cross-layer relationships to Cisco inventory

### Phase 4: reporting

- build Power BI measures and quality indicators
- document limitations and collection frequency
- publish only reviewed screenshots without private identifiers

## Repository boundaries

| Concern | Repository |
|---|---|
| Physical switch, VLAN and trunk configuration | `cisco-switching-lab` |
| Hypervisor, VM/LXC, storage, backup and API setup | `proxmox-virtualization-lab` |
| Sanitized data model, SQL checks and Power BI | `network-operations-data-lab` |

## Portfolio standard

The value of this integration comes from traceability: source definition, collection boundary, data model, validation rules, reporting logic and explicit limitations. A screenshot of the Proxmox web interface alone is not considered a meaningful Data/BI artifact.