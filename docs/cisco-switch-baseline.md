# Cisco Switch Baseline

This document describes the public-safe baseline for a small Cisco switching lab.

The goal is not to publish real device configuration, but to document the learning setup, validation steps and operational data concepts in an anonymized way.

## Scope

The lab uses a compact Cisco Catalyst switch as a local CCNA-level switching platform.

The current baseline focuses on:

- basic Layer 2 switching
- local management access
- SSH-based administration
- public-safe interface documentation
- later VLAN and trunking exercises
- later collection of sanitized operational data

## Current baseline state

The hardware baseline has been verified in a local home-lab environment.

Verified capabilities:

- switch boots successfully
- local console access works
- management SVI receives an address via DHCP
- connected client ports negotiate at 1 Gbit/s full duplex
- local router is reachable from the switch
- connected clients can access the network through the switch
- SSH access is enabled for local management
- Telnet is disabled
- HTTP and HTTPS web management are disabled
- automatic configuration download and provisioning features are disabled for the lab context

## Management model

The switch is managed through:

- local console access for recovery and initial setup
- SSH for normal local administration

The web interface is intentionally not used.

## Public-safe handling

Real configuration exports must not be committed to this repository.

Do not publish:

- real serial numbers
- real MAC addresses
- real hostnames
- real management IP addresses
- public IP addresses
- Tailscale IP addresses
- password hashes
- user secrets
- full running-config or startup-config outputs from real devices

Only sanitized examples and synthetic sample data should be used.

## Useful verification commands

The following commands are useful for documenting the lab state without publishing sensitive raw output:

```text
show version
show boot
show ip interface brief
show interfaces status
show vlan brief
show running-config | section line vty
show running-config | include ip http|ip ssh|domain-lookup
show users
```

Any resulting output must be reviewed and sanitized before publication.

## Next steps

Planned next steps:

1. stabilize the final home-network topology
2. assign a stable management address through the router DHCP reservation
3. add public-safe interface descriptions
4. document VLAN 10 / VLAN 20 / VLAN 30 as a lab roadmap
5. collect only sanitized or synthetic operational data for analysis
