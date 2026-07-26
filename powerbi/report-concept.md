# Power BI Report Concept

## Purpose

The first report should explain the current static network-operations sample without implying live monitoring.

Primary audience:

- a technical interviewer
- a BI or process-analysis reviewer
- a small infrastructure team reviewing documentation quality

## Current source model

```text
devices 1 ────< interfaces
devices 1 ────< topology_links
interfaces 1 ────< topology_links through the source interface
```

The public report CSV is a separate derived table with one row per executed check result.

## Proposed report pages

### 1. Infrastructure Overview

Questions:

- how many devices are represented?
- which device roles exist?
- how many interfaces and topology links exist?
- what is the documentation coverage?

Suggested visuals:

- device count card
- interface count card
- topology-link count card
- devices by role
- documentation-coverage KPI

### 2. Interface Operations

Questions:

- which administrative and operational status combinations exist?
- how many interfaces are active?
- which port roles are represented?
- are there operational warnings?

Suggested visuals:

- interface status matrix
- interfaces by port role
- operational-warning card
- filtered interface detail table using synthetic identifiers

### 3. Topology Coverage

Questions:

- how many active relationships are documented?
- which link roles exist?
- do all modeled links resolve to known devices and source interfaces?

Suggested visuals:

- links by role and status
- source-to-target relationship table
- unresolved relationship count

### 4. Data Quality

Questions:

- did structural data-quality rules pass?
- which categories contain findings?
- how many operational warnings require review?
- is the committed report current?

Suggested visuals:

- data-quality pass rate
- failed data-quality check count
- operational warning count
- check results by category and status
- descriptions for non-OK results

## Candidate measures

Conceptual measures:

```text
Device Count
Interface Count
Topology Link Count
Active Interface Count
Operational Warning Count
Data Quality Failure Count
Data Quality Pass Rate %
Description Coverage %
```

The exact DAX should be written only after the local model and field types are confirmed in Power BI.

## Filtering

Useful filters:

- device role
- device type
- interface port role
- administrative status
- operational status
- link role
- check category
- check status

## Semantic distinction

Do not combine `FAIL` and `WARN` into one undifferentiated error count.

- `FAIL` means source-data quality did not meet a rule.
- `WARN` means the source data may be correct but describes an operational condition requiring review.
- `INFO` is descriptive.

## Current limitations

- the sample is static
- there is no refresh history
- there are only five devices, five interfaces and three links
- no real addresses, MAC values or serial numbers exist
- interface errors and traffic counters are not modeled
- no Proxmox live data exists
- the report should not be presented as real-time monitoring

## Publication rule

A screenshot or template may be published only after:

1. all fields are public-safe
2. no local paths or account names are visible
3. the model matches the documented grain and relationships
4. limitations are visible
5. the screenshot adds more evidence than the existing Markdown concept
