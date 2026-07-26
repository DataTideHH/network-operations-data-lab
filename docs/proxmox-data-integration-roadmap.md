# Proxmox Data Integration Roadmap

## Current status

The separate [`proxmox-virtualization-lab`](https://github.com/DataTideHH/proxmox-virtualization-lab) repository contains a validated pre-hardware design, public-safety rules, a synthetic inventory example and a tested validator.

A dedicated x86 host, operational Proxmox installation and live API source do not currently exist.

This document therefore remains a source-integration roadmap. It does not claim live virtualization data.

## Initial reviewed boundary

The current pre-hardware public schema `0.1` covers only:

- nodes
- guests

Storage, network-assignment and backup-run entities remain deferred until real API fields and source semantics have been reviewed.

## Proposed node grain

One row per sanitized node at one collection state.

Candidate fields:

```text
node_key
node_status
cpu_threads
memory_total_mb
storage_total_gb
source_observed_at_utc
collected_at_utc
collection_run_key
```

## Proposed guest grain

One row per sanitized VM or LXC guest at one collection state.

Candidate fields:

```text
guest_key
node_key
guest_type
guest_status
purpose_category
owner_role
cpu_allocated
memory_allocated_mb
backup_policy_key
source_observed_at_utc
collected_at_utc
collection_run_key
```

Keys must be synthetic public identifiers, not real node names, VM IDs or storage IDs.

## Initial quality rules

### Completeness

- each node and guest has a stable synthetic key
- each guest has a reviewed type and lifecycle status
- each non-temporary guest has a purpose and owner role
- required collection timestamps are present

### Relationships

- each guest references a known node
- collection-run relationships are complete
- no orphan guest rows exist

### Validity

- guest types use reviewed values such as `qemu` and `lxc`
- CPU and memory values are non-negative
- source timestamps are not later than collection timestamps
- status values use controlled vocabularies

### Freshness

- collection age is measurable
- reporting distinguishes source observation from collection time
- stale collection runs are flagged against a documented threshold

## Extraction principles

After hardware exists:

1. use a dedicated least-privilege API token
2. review exact API paths and fields
3. collect raw responses privately
4. keep token secrets and raw payloads outside Git
5. separate collection from sanitization
6. preserve source and collection timestamps
7. map private identifiers to synthetic public keys
8. compare actual fields with the planned schema
9. revise the model before publishing examples
10. document API and release assumptions

## Deferred source entities

These may be added only after live field review:

- storage inventory
- virtual network assignments
- backup events and policies
- snapshot lifecycle
- resource utilization observations
- extraction-run metadata beyond the minimum collection key

## Implementation phases

### Phase 0 — current

- maintain the reviewed nodes-and-guests schema boundary
- keep public examples synthetic
- do not claim live extraction

### Phase 1 — dedicated host and private source review

- install and validate the separate Proxmox lab
- create a least-privilege read-only token
- collect one private sample
- inspect actual fields and null behavior
- document source semantics

### Phase 2 — local analytical integration

- map reviewed data to SQLite staging tables
- add referential and freshness checks
- compare network and virtualization collection grains
- keep private identifiers outside the public repository

### Phase 3 — public-safe portfolio sample

- publish only synthetic or reviewed sanitized examples
- document transformation and limitations
- extend the Power BI concept with virtualization pages
- publish screenshots only after privacy review

## Repository boundaries

| Concern | Repository |
|---|---|
| physical switching and VLAN configuration | `cisco-switching-lab` |
| Proxmox installation, guests, storage, backup and API access | `proxmox-virtualization-lab` |
| sanitized source model, SQLite, SQL, quality checks and BI | `network-operations-data-lab` |

The analytical value comes from traceability across source definition, collection boundary, model, validation and reporting—not from a Proxmox web-interface screenshot.
