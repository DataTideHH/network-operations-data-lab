# Lab Topology

This document describes the current and planned lab topology in a public-safe way.

## Current public-safe example topology

```text
Client devices
     |
     | Ethernet / Wi-Fi
     |
Home router / lab gateway
     |
     | Ethernet
     |
Cisco lab switch
     |
     | Access ports
     |
Lab clients / test devices
```

The current verified data source is the Cisco switching lab. No Proxmox host is currently part of the implemented topology.

## Future cross-layer topology

```text
Existing home LAN
     |
     | isolated lab path
     |
Cisco lab router / gateway
     |
     | VLANs and controlled switch ports
     |
Cisco lab switch
     |
     | initial access port, later optional 802.1Q trunk
     |
future dedicated Proxmox host
     |
     | virtual networks
     |
VMs / LXC containers
     |
     | REST API and sanitized exports
     |
network-operations-data-lab
     |
     | Python / SQLite / SQL
     |
Power BI reporting concept
```

The future Proxmox host shown here is a roadmap item pending suitable dedicated x86 hardware. The diagram does not claim a working installation.

## Data-flow boundaries

- the Cisco repository owns physical ports, VLANs, trunks and switch verification
- the future Proxmox repository owns hypervisor, virtual network, guest, storage and backup documentation
- this repository owns sanitized exports, data modelling, data-quality checks and BI-oriented outputs

## Privacy note

Do not publish real values for:

- public IP addresses
- private management IP addresses
- Tailscale IP addresses
- real MAC addresses
- serial numbers
- personal hostnames
- ISP account details
- full production-like configurations
- Proxmox node, cluster or guest names derived from real systems
- API tokens, ticket cookies, fingerprints or backup credentials

Use anonymized names such as:

- `lab-switch-01`
- `client-01`
- `pve-node-01`
- `vm-data-01`
- `lxc-tools-01`
- `vlan-10-users`
- `vlan-20-lab`
- `vlan-30-servers`
- `vlan-99-management`