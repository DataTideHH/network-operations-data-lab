# Scripts

Python helper scripts for the network operations data lab.

The scripts are intentionally small and readable. They currently use only the Python standard library so the workflow remains easy to inspect and does not require a separate dependency setup.

## Current scripts

- `load_sample_data.py`
- `run_data_quality_checks.py`

## `load_sample_data.py`

Loads the public-safe sample CSV files from `data/sample/`, prints the records and calculates simple summaries such as:

- device counts
- interface operational status counts
- port role counts

Run:

`python scripts/load_sample_data.py`

## `run_data_quality_checks.py`

Runs a public-safe data-quality check workflow aligned with the numbered checks in `sql/data_quality_checks.sql`.

Input files:

- `data/sample/devices.csv`
- `data/sample/interfaces.csv`

Output file:

- `data/processed/data_quality_report.csv`

The report contains only aggregated check metadata:

- check number
- check name
- category
- status
- affected row count
- short description

It does not write device names, interface names or row-level identifiers.

The duplicate checks count affected rows in the Python report, while the SQL version returns duplicate groups. Missing values are handled by the dedicated missing-value checks and are not double-counted as duplicates.

The current sample report contains one expected finding for check 11 because the synthetic interface sample includes an administratively up but operationally down interface. This is useful as a small demonstration that the validation workflow detects an operational data-quality issue.

Run:

`python scripts/run_data_quality_checks.py`
