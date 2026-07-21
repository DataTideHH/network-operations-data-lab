# Project Scope

## Purpose

This project connects infrastructure operations with data analysis, data quality and BI reporting.

It is not intended to replace the separate technical labs. Instead, it adds the data layer above networking and, later, virtualization practice.

## Relationship to other repositories

- `cisco-switching-lab` focuses on physical Cisco switching concepts, device configuration, VLANs, trunks and lab documentation.
- the planned [`proxmox-virtualization-lab`](https://github.com/DataTideHH/proxmox-virtualization-lab) will focus on a future dedicated x86 virtualization host, virtual machines, LXC containers, storage, backups, permissions and API access.
- `network-operations-data-lab` focuses on collecting, structuring, analyzing and visualizing sanitized operational data from those infrastructure layers.

The Proxmox repository and live data source are not implemented yet. Until suitable hardware exists, this project should contain only reviewed schemas, synthetic examples and clearly labelled integration plans.

## Initial phase

The current phase should stay simple:

1. Define sample network inventory data.
2. Define sample interface status data.
3. Load the data with Python.
4. Prepare it for SQL analysis.
5. Build simple BI-style summary tables.
6. Load the current model into SQLite.
7. Later: visualize selected KPIs in Power BI.

## Future Proxmox phase

After the separate virtualization lab is installed and validated:

1. Define the API extraction boundary and least-privilege token requirements.
2. Export only required node, guest, storage, network and backup metadata.
3. Sanitize identifiers before publishing examples.
4. Preserve source timestamps and collection timestamps separately.
5. Load the data into normalized staging tables.
6. Run referential, completeness, freshness and policy checks.
7. Build cross-layer infrastructure KPIs only after source semantics are understood.

## Possible future KPIs

### Network operations

- number of devices by role
- active vs inactive interfaces
- access vs trunk ports
- VLAN usage
- interface error counters
- devices with missing documentation
- outdated configuration snapshots

### Virtualization operations

- nodes and guests by status
- allocated versus observed CPU and memory
- guests without documented owner or purpose
- guests without an assigned backup policy
- backup freshness and failed backup counts
- storage capacity and utilization
- stale or orphaned inventory relationships
- management and guest network assignment coverage

## Out of scope

- publishing raw real infrastructure exports
- publishing credentials, API tokens, private addresses or production-like topology
- claiming live Proxmox collection before a dedicated host exists
- presenting the project as an enterprise monitoring platform
- inflating a small learning lab into an enterprise-scale architecture