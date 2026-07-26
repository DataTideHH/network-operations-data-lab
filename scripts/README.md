# Scripts

The current workflow uses only the Python standard library.

## Architecture

```text
workflow.py
    shared CSV, SQLite and report functions

load_sample_data.py
    inspect the three CSV contracts and summaries

build_sqlite_database.py
    build the local SQLite database

run_sqlite_analysis.py
    build a temporary database and print analysis views

run_data_quality_checks.py
    build a temporary database and write the public report
```

Run commands from the repository root with module syntax.

## Inspect the sample data

```bash
python -m scripts.load_sample_data
```

The command verifies all three ordered headers and prints counts for:

- devices
- interfaces
- topology links
- interface operational status
- port roles
- link status

## Build SQLite locally

```bash
python -m scripts.build_sqlite_database
```

Default output:

```text
data/processed/network_operations.db
```

The database file is ignored by Git.

Alternative path:

```bash
python -m scripts.build_sqlite_database --database path/to/lab.db
```

Use `--no-replace` to prevent replacement of an existing database.

## Run analysis views

```bash
python -m scripts.run_sqlite_analysis
```

This command uses a temporary database and leaves no binary artifact in the repository.

## Generate the quality report

```bash
python -m scripts.run_data_quality_checks
```

Output:

```text
data/processed/data_quality_report.csv
```

Strict mode:

```bash
python -m scripts.run_data_quality_checks --strict
```

Strict mode returns exit code `2` only when a `data_quality` rule has `FAIL`. Operational warnings remain review items and do not make the workflow technically fail.

## Exit codes

```text
0  completed successfully
1  file, contract, conversion, SQLite or execution error
2  strict-mode data-quality failure
```

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

No `requirements.txt` is needed.
