# SQL

SQL queries for analyzing structured network operations data.

Initial focus:

- device inventory analysis
- interface status summaries
- VLAN and port role reporting

## Current SQL files

- `sample_analysis.sql` contains first reporting-oriented sample queries.
- `data_quality_checks.sql` contains data-quality checks for completeness, consistency and BI readiness.

The data-quality checks are based on the current public-safe sample CSV structure:

- `devices`: `device_id`, `device_name`, `device_type`, `vendor`, `model`, `role`, `location`
- `interfaces`: `device_name`, `interface_name`, `interface_type`, `admin_status`, `oper_status`, `vlan`, `port_role`, `description`

