# Data Model

## Current model status

The current public model is a static, synthetic Cisco-oriented baseline. It is not a historical monitoring feed and does not claim live collection.

The implemented source tables are:

- `devices`
- `interfaces`
- `topology_links`

The aggregated `data_quality_report` is a derived reporting artifact.

## Grain and keys

| Entity | Grain | Primary key |
|---|---|---|
| `devices` | one row per synthetic infrastructure device | `device_id` |
| `interfaces` | one row per interface in the current sample baseline | `interface_id` |
| `topology_links` | one row per directed documented relationship | `link_id` |
| `data_quality_report` | one row per executed reporting rule | check number plus check name |

`device_id`, `interface_id` and `link_id` are synthetic public identifiers. They must not be copied from private infrastructure.

## Relationships

```text
devices 1 ────< interfaces

devices 1 ────< topology_links.source_device_id
devices 1 ────< topology_links.target_device_id

interfaces 1 ────< topology_links
                    through
                    source_device_id + source_interface_id
```

A modeled source interface must exist in `interfaces`.

A target device must exist in `devices`. `target_interface_id` may contain the public placeholder `unknown` when the endpoint device is represented but its individual interface is outside the current model.

## Device attributes

| Field | Meaning |
|---|---|
| `device_id` | synthetic stable technical key |
| `device_name` | public-safe descriptive name |
| `device_type` | reviewed device-class value |
| `vendor` | public-safe vendor label |
| `model` | public-safe model label |
| `role` | analytical device role |
| `location` | generalized lab location |
| `location_scope` | controlled location classification |
| `management_scope` | whether the device is managed, an endpoint or unmanaged |
| `is_active` | Boolean current-baseline flag |

Current controlled values include:

```text
device_type:
switch
router
wireless_bridge
client

role:
access_switch
edge_router
media_bridge
lab_client

location_scope:
home_lab
external_lab

management_scope:
managed
endpoint
unmanaged
```

## Interface attributes

| Field | Meaning |
|---|---|
| `interface_id` | synthetic stable technical key |
| `device_id` | foreign key to `devices` |
| `device_name` | duplicated descriptive attribute for source readability |
| `interface_name` | public-safe interface label |
| `interface_type` | interface technology or class |
| `admin_status` | configured state |
| `oper_status` | observed operational state in the sample baseline |
| `vlan` | VLAN or trunk documentation field |
| `port_role` | analytical interface role |
| `speed_mbps` | non-negative negotiated or documented speed |
| `duplex` | documented duplex state |
| `description` | public-safe port description |
| `description_present` | Boolean documentation flag |
| `expected_downstream_devices` | expected relationship cardinality |

`device_id` is the relationship key. `device_name` is not the authoritative join key. A quality rule verifies that the duplicated name matches the referenced device.

Current controlled values include:

```text
admin_status:
up
down

oper_status:
up
down
notconnect
unknown

port_role:
access
trunk
uplink
client_access
lab_access
bridge_uplink

duplex:
full
half
unknown

expected_downstream_devices:
none
single
multiple
```

## Topology-link attributes

| Field | Meaning |
|---|---|
| `link_id` | synthetic stable technical key |
| `source_device_id` | source device foreign key |
| `source_interface_id` | source interface within the source device |
| `target_device_id` | target device foreign key |
| `target_interface_id` | modeled interface ID or `unknown` placeholder |
| `link_role` | analytical relationship role |
| `link_status` | active, inactive or planned |
| `expected_downstream_devices` | relationship-cardinality expectation |

Topology rows are directed for analytical clarity. The current sample does not automatically create a reverse row.

## Hard validation and report checks

The workflow has two validation layers.

### Load-time contract

Python and SQLite reject:

- missing or reordered CSV headers
- invalid Boolean text
- invalid non-negative integer text
- primary-key violations
- foreign-key violations
- uniqueness violations
- values outside SQLite `CHECK` constraints

These are technical workflow errors and stop database publication.

### Reporting rules

SQL produces aggregated:

- data-quality checks
- operational-condition checks
- summary metrics

A correct record may still describe an undesirable operational condition. For example, an interface can be accurately recorded as administratively up and operationally down. That is a warning for review, not automatically bad source data.

## Current temporal limitation

The current tables describe one static sample state. They do not support trend analysis.

A later snapshot model may add:

```text
snapshot_key
source_observed_at_utc
collected_at_utc
collection_run_key
```

Those fields should be introduced only when collection semantics and retention requirements are defined.

## Future Proxmox boundary

The separate Proxmox pre-hardware schema `0.1` currently covers nodes and guests. This repository should not add storage, network-assignment or backup-run entities until the actual API fields and source semantics have been reviewed on a real lab host.
