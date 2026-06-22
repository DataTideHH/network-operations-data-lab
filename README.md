# Network Operations Data Lab

Network Operations Data Lab is a learning and portfolio project that connects networking fundamentals with a Data/BI workflow.

The goal is not only to configure network devices, but to treat network operations as a structured data source.

## Project idea

This lab explores how operational network data can be collected, cleaned, modeled, queried and visualized.

Planned data sources include:

- device inventory
- interface status
- VLAN documentation
- trunk/access port information
- error counters
- configuration snapshots
- basic availability checks
- lab topology documentation

## Planned stack

- Cisco switching and routing lab
- Python for parsing and data preparation
- CSV and SQLite for structured storage
- SQL for analysis and validation
- Power BI for reporting and dashboard prototypes
- Markdown documentation for reproducibility

## Current focus

This project is currently in an early learning-lab stage.

The first phase is aligned with CCNA-level networking fundamentals:

- switching basics
- VLANs
- trunk ports
- STP basics
- interface documentation
- subnetting and Layer 3 concepts
- network troubleshooting notes

## Data and privacy

This repository is designed to be public-safe.

Real device identifiers, MAC addresses, public IP addresses, Tailscale IPs, serial numbers, hostnames and private network details must not be published here.

All examples should use anonymized or sample data.

## Why this project matters

For Data/BI work, operational IT systems are important data sources.

This project demonstrates how infrastructure data can be transformed into useful reporting structures, combining:

- networking fundamentals
- data preparation
- SQL-based analysis
- BI-style visualization
- technical documentation

## Repository structure

    network-operations-data-lab/
    ├── data/
    │   ├── sample/
    │   └── processed/
    ├── docs/
    ├── powerbi/
    ├── scripts/
    ├── sql/
    ├── .gitignore
    └── README.md

## Status

Early lab / in progress.

This repository is connected to my Data/BI Analyst track and my CCNA preparation.
