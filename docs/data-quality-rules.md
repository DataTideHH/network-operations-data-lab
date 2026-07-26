# Data Quality Rules

## Purpose

The current workflow validates a public-safe three-table network-operations model before it is used for SQL analysis or BI reporting.

Inputs:

- `data/sample/devices.csv`
- `data/sample/interfaces.csv`
- `data/sample/topology_links.csv`

Derived output:

- `data/processed/data_quality_report.csv`

## Validation architecture

### 1. Structural and type validation

Python enforces:

- exact ordered CSV headers
- non-empty input files
- explicit Boolean conversion
- explicit non-negative integer conversion

SQLite then enforces:

- primary keys
- foreign keys
- unique relationships
- controlled-value `CHECK` constraints
- non-negative speed values

Structural or load failures stop the workflow with a non-zero exit code.

### 2. Aggregated SQL checks

`sql/data_quality_checks.sql` creates `data_quality_results`.

The public report contains only aggregated metadata. It does not expose row-level device, interface or topology identifiers.

## Categories and statuses

| Category | Status values | Interpretation |
|---|---|---|
| `data_quality` | `OK`, `FAIL` | completeness, validity, uniqueness or relationship integrity |
| `operational_condition` | `OK`, `WARN` | plausible source data describing an operational exception |
| `summary` | `INFO` | descriptive counts |

This distinction prevents operational state from being confused with source-data quality.

## Current rule groups

### Inventory and identifier rules

- required device and interface identifiers
- duplicate identifiers
- required descriptive device attributes
- controlled device scopes and active-state values
- interface-to-device relationship validity
- consistency between `device_id` and duplicated `device_name`

### Interface rules

- required names, type, statuses and VLAN documentation
- controlled administrative and operational status values
- controlled port-role and duplex values
- non-negative and plausible speed values
- description and `description_present` consistency
- expected downstream cardinality by role

### Topology rules

- required and unique `link_id`
- known source device and interface
- known target device
- validation of specific modeled target interfaces
- controlled link role and link status
- matching source-interface and link roles
- duplicate directed relationship detection
- active-link source-interface status

### Operational conditions

The current sample deliberately contains:

```text
one interface with admin_status=up and oper_status=down
```

This produces:

```text
category = operational_condition
status   = WARN
```

It does not produce a data-quality failure because the record is complete, valid and internally consistent.

## Report reproducibility

Run:

```bash
python -m scripts.run_data_quality_checks
```

CI reruns the command and verifies:

```bash
git diff --exit-code -- data/processed/data_quality_report.csv
```

A source-data or rule change therefore requires a matching committed report update.

## Strict mode

The report command supports:

```bash
python -m scripts.run_data_quality_checks --strict
```

Exit codes:

```text
0  workflow succeeded and no data_quality FAIL exists
1  file, schema, type, SQLite or execution error
2  workflow succeeded but at least one data_quality FAIL exists
```

Operational warnings do not trigger strict-mode failure.

## BI interpretation

A reporting layer should expose data quality and operational exceptions separately.

Recommended measures include:

- data-quality pass rate
- failed data-quality check count
- operational warning count
- documented-interface coverage
- orphan relationship count
- active interface count

A single combined red/green score would hide the distinction between incorrect data and a correctly observed infrastructure condition.
