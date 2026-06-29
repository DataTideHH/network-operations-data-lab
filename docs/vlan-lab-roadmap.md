# VLAN Lab Roadmap

This document describes the planned VLAN structure for the Cisco switching lab.

The goal is to learn VLAN design, access ports, trunks, management SVIs and troubleshooting without disrupting the productive home network.

## Planned VLAN model

| VLAN | Name | Purpose |
|---:|---|---|
| 10 | MGMT | Management network for switch and future lab infrastructure |
| 20 | CLIENTS | Normal client devices in a controlled lab scenario |
| 30 | LAB_IOT | Lab devices, test nodes and future isolated experiments |
| 999 | NATIVE_UNUSED | Unused native VLAN for trunk hardening practice |

## Important design note

The current home router remains responsible for normal internet access, DHCP and DNS.

The VLAN roadmap will be implemented incrementally. Productive client connectivity should not be moved until the router, switch and remote access paths are stable.

## Phase 1: Create VLANs only

Create the VLANs without changing productive access ports.

Example:

```text
configure terminal
vlan 10
 name MGMT
vlan 20
 name CLIENTS
vlan 30
 name LAB_IOT
vlan 999
 name NATIVE_UNUSED
end
write memory
```

Validation:

```text
show vlan brief
```

## Phase 2: Test access ports

Use unused switch ports for lab-only testing.

Example:

```text
configure terminal
interface gi0/4
 description LAB_CLIENT_ACCESS_VLAN20
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast

interface gi0/5
 description LAB_NODE_ACCESS_VLAN30
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
end
write memory
```

Validation:

```text
show interfaces status
show vlan brief
show mac address-table
```

## Phase 3: Management VLAN

Move switch management away from VLAN 1 only after the lab topology is stable.

Example concept:

```text
interface vlan 10
 description MANAGEMENT_SVI
 ip address <sanitized-management-ip> <sanitized-mask>
 no shutdown
```

This requires a valid routing and reachability plan. It should not be implemented blindly.

## Phase 4: Trunking practice

Use a lab-only trunk to a second switch, router, Linux host, hypervisor or VLAN-aware firewall.

Example concept:

```text
interface gi0/8
 description LAB_TRUNK
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,30
```

Validation:

```text
show interfaces trunk
show vlan brief
show spanning-tree
```

## Phase 5: Operational data collection

Once the lab is stable, sanitized outputs can be transformed into structured data.

Candidate data sources:

- interface status
- VLAN membership
- trunk configuration
- MAC address table summaries
- STP state summaries
- device inventory without real identifiers
- basic availability checks

All collected data must be anonymized before it is used in this public repository.
