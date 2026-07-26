# VLAN Lab Roadmap

## Status and repository boundary

This document mirrors the planned VLAN roles from `cisco-switching-lab`. It exists here only to keep the operational data model aligned with the network design.

Cisco CLI implementation and validation belong in the Cisco repository.

## Planned VLAN roles

| VLAN | Role | Intended analytical label |
|---:|---|---|
| 10 | test clients | `TEST_CLIENTS` |
| 20 | lab systems | `LAB_SYSTEMS` |
| 30 | test services and servers | `TEST_SERVICES` |
| 99 | management | `MGMT` |
| 998 | unused native VLAN for lab trunks | `NATIVE_UNUSED` |
| 999 | parking VLAN for shut unused access ports | `BLACKHOLE` |

## Design rules

- VLAN 99 is the planned management VLAN.
- VLAN 998 is used only as the matching unused native VLAN on both trunk ends.
- VLAN 998 has no SVI and no connected endpoint.
- VLAN 999 is reserved for administratively shut unused access ports.
- VLAN 999 is not the trunk native VLAN.
- Productive home-network connectivity is not moved during early lab phases.
- Console or independent recovery access is retained before management or trunk changes.

## Phase 1: define VLANs without moving active ports

Conceptual Cisco-side configuration:

```text
vlan 10
 name TEST_CLIENTS
vlan 20
 name LAB_SYSTEMS
vlan 30
 name TEST_SERVICES
vlan 99
 name MGMT
vlan 998
 name NATIVE_UNUSED
vlan 999
 name BLACKHOLE
```

Validation belongs in `cisco-switching-lab` and should include the effective VLAN table before any access-port change.

## Phase 2: isolated access-port tests

Use only unused lab ports.

Conceptual assignments:

```text
test client port    -> VLAN 10
lab system port     -> VLAN 20
test service port   -> VLAN 30
unused shut port    -> VLAN 999
```

The data model should capture:

- interface identifier
- port role
- VLAN assignment
- administrative state
- operational state
- public-safe description

## Phase 3: management VLAN

Move management from VLAN 1 only after:

- local console recovery is confirmed
- routing and reachability are planned
- the existing management path is documented
- rollback steps are available

The planned management SVI belongs to VLAN 99, not VLAN 10.

## Phase 4: lab-only trunk

Conceptual trunk design:

```text
allowed VLANs: 10,20,30,99
native VLAN:   998
```

VLAN 999 remains excluded from normal trunk use.

Data-quality checks should later verify:

- documented allowed VLANs
- native VLAN consistency
- no SVI or endpoint assignment on VLAN 998
- unused ports assigned to VLAN 999 and administratively down

## Phase 5: operational data collection

After the network stage is verified, public-safe source records may include:

- interface status summaries
- VLAN membership
- trunk role and allowed-VLAN documentation
- STP state summaries
- MAC-table counts without real addresses
- error-counter summaries
- configuration snapshot timestamps

No raw private output should be committed.
