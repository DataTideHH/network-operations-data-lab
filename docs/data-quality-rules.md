# Data Quality Rules

This document describes the first public-safe data-quality checks for the Network Operations Data Lab.

The goal is to treat network documentation as structured operational data. Before this data can be used for SQL analysis or BI reporting, it should be checked for completeness, consistency and basic plausibility.

## Current sample data

Current sample inputs:

- `data/sample/devices.csv`
- `data/sample/interfaces.csv`

Current device columns:

    device_id, device_name, device_type, vendor, model, role, location

Current interface columns:

    device_name, interface_name, interface_type, admin_status, oper_status, vlan, port_role, description

## Public-safe data rule

The sample data must not contain real sensitive infrastructure details.

Do not publish:

- real serial numbers
- real MAC addresses
- real public IP addresses
- private hostnames
- Tailscale IP addresses
- customer-specific identifiers
- production configuration snippets

Use anonymized lab names and synthetic examples instead.

## Device inventory checks

Recommended checks:

- device inventory exists
- device inventory is not empty
- `device_id` is complete
- `device_id` is unique
- `device_name` is complete
- `device_name` is unique
- `device_type`, `vendor`, `model`, `role` and `location` are documented

## Interface documentation checks

Recommended checks:

- interface inventory exists
- interface inventory is not empty
- `device_name` is complete
- `interface_name` is complete
- each `device_name` + `interface_name` combination is unique
- `admin_status` and `oper_status` are documented
- `port_role` is documented
- `description` is documented where useful

## Relationship checks

Recommended checks:

- every interface references a known `device_name` from `devices.csv`
- device names are consistent between both files
- no orphan interfaces exist

## Reporting-oriented checks

Recommended checks:

- interfaces administratively up but operationally down
- access ports without VLAN documentation
- trunk ports without trunk documentation
- missing interface descriptions
- status and port-role summaries for BI reporting

## Why this matters for BI

Power BI reports and SQL analysis depend on reliable source data.

If device identifiers, interface names, port roles or VLAN documentation are incomplete, dashboards can become misleading. These checks are intentionally simple and transparent so they can be explained in a learning, portfolio and interview context.

## Current limitations

This is an early learning-lab implementation.

The current checks are based on public-safe sample CSV files. Later versions may add:

- SQLite table creation
- automated Python data-quality reports
- additional SQL validation queries
- Power BI dashboard prototypes
- documented remediation notes
