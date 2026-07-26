# Lab Topology

## Current implemented data source

The current public model represents a sanitized Cisco-oriented baseline:

```text
generalized home or lab gateway
            |
            v
public-safe wireless or media bridge
            |
            v
Cisco lab switch
       |          |
       v          v
lab client A   lab client B
```

The committed data model represents:

- five synthetic devices
- five interfaces
- three directed topology links

It omits real addressing, hardware identifiers, account details and full private topology.

## Current data flow

```text
devices.csv
interfaces.csv
topology_links.csv
        |
        v
Python contract validation
        |
        v
SQLite keys and constraints
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

## Future cross-layer topology

```text
existing home LAN
        |
        | controlled lab path
        v
future lab router or gateway
        |
        v
Cisco lab switch
        |
        | access port first
        | optional later 802.1Q trunk
        v
future dedicated Proxmox host
        |
        v
VMs and LXC containers
        |
        | private raw API collection
        v
review and sanitization boundary
        |
        v
network-operations-data-lab
```

The separate Proxmox repository contains a validated pre-hardware design. No dedicated host or live API source is currently implemented.

## Repository ownership

| Layer | Owning repository |
|---|---|
| physical switch, IOS, VLAN and trunk validation | `cisco-switching-lab` |
| hypervisor, guests, storage, backup and API access | `proxmox-virtualization-lab` |
| sanitized model, SQLite, SQL, quality checks and BI | `network-operations-data-lab` |

## Privacy boundary

Do not publish:

- real private or public addresses
- MAC addresses
- serial numbers
- private hostnames
- API tokens or ticket cookies
- cluster fingerprints
- raw configuration exports
- complete private topology
- backup credentials

Use synthetic identifiers such as:

```text
dev-001
int-001
link-001
pve-node-01
vm-data-01
```
