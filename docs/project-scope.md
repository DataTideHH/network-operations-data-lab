# Project Scope

## Purpose

This project connects network operations with data analysis and BI reporting.

It is not intended to replace the separate Cisco Switching Lab. Instead, it adds the data layer above networking practice.

## Relationship to other repositories

- `cisco-switching-lab` focuses on Cisco switching concepts, device configuration and lab documentation.
- `network-operations-data-lab` focuses on collecting, structuring, analyzing and visualizing network operations data.

## Initial phase

The initial phase should stay simple:

1. Define sample network inventory data.
2. Define sample interface status data.
3. Load the data with Python.
4. Prepare it for SQL analysis.
5. Build simple BI-style summary tables.
6. Later: visualize selected KPIs in Power BI.

## Possible future KPIs

- number of devices by role
- active vs inactive interfaces
- access vs trunk ports
- VLAN usage
- interface error counters
- devices with missing documentation
- outdated configuration snapshots
