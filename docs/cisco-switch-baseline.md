# Cisco Switch Baseline

## Purpose

This document describes the public-safe source context for the current data workflow. Detailed Cisco procedures and verified device maintenance belong in [`cisco-switching-lab`](https://github.com/DataTideHH/cisco-switching-lab).

## Verified source context

The private physical lab has verified:

- local console access
- SSH administration
- stable management reachability
- active Gigabit Ethernet links
- public-safe interface descriptions
- gateway and external reachability
- disabled Telnet and web management
- saved baseline configuration

Real hostnames, addresses, serial numbers, MAC addresses, credentials and full configurations are excluded.

## Current public data artifacts

The network data repository now implements:

- synthetic device inventory
- synthetic interface baseline
- synthetic topology relationships
- exact CSV contracts
- SQLite loading and constraints
- SQL analysis and quality views
- an aggregated public-safe report
- automated tests and CI

The topology and port-description fields are no longer future tasks; they are part of the implemented model.

## Current limitations

- the public sample is static
- no raw CLI output is committed
- no interface error-counter snapshot is yet modeled
- no historical collection timestamps exist
- VLAN 10/20/30/99/998/999 remain a planned segmented lab stage
- Proxmox remains a future source

## Next source expansion

A useful next network-data increment would be one reviewed snapshot table with:

- a synthetic snapshot key
- source observation time
- collection time
- selected interface status or counter values
- documented sanitization rules

That extension should be added only after the snapshot grain and retention purpose are defined.
